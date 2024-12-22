import re
import os
from json import dumps
from bs4 import BeautifulSoup
from utils import extract_filename
from css import get_styles_by_class
from image import save_image
from globals import assets, assets_html
from progress import Progress


used_images: list[str] = []


def parse_text_element(item, cl):
    el = item.find("p", class_=cl)
    result = el and el.text.strip().replace('"', '')
    return result


def parse_number_element(item, cl):
    el = item.find("p", class_=cl)
    content = el and el.text
    parts = content and content.split(' ')
    result = parts and int(parts[1])
    return result


def parse_item_id(item):
    id_el = item.find('p', class_='r-itemid')
    content = id_el and id_el.text.strip()
    if content is None:
        return None
    parts = content.split(': ')
    prefix = parts[0].lower()
    value = parts[-1]
    item_id = f"{prefix}-{value}"
    return item_id


def parse_item_content(item):
    el = item.find('span')
    lines = []
    for p in el.find_all('p', class_=False):
        if p.find_parent('ul') is None:
            lines.append(p.get_text())
    return "\n".join(lines)


def parse_items_params(item):
    lines = item.find('ul').find_all('p') if item.find('ul') else []
    item_type = None
    item_pool = None
    recharge_time = None
    for p in lines:
        text = p.get_text()
        if "Type" in text:
            item_type = text.split(': ')[-1]
        if "Pool" in text:
            item_pool = text.split(': ')[-1]
        if "Recharge" in text:
            recharge_time = text.split(': ')[-1]
    return {
        "type": item_type,
        "item_pool": item_pool,
        "recharge_time": recharge_time,
    }


def parse_position(value):
    if not value:
        return [0, 0]
    parts = value.split()
    x = int(parts[0].replace("px", ""))
    y = int(parts[1].replace("px", ""))
    return [abs(x), abs(y)]


def parse_size(pos=None, item=None):
    pos = pos or {}
    item = item or {}
    width = pos.get('width') or item.get('width')
    height = pos.get('height') or item.get('height')
    w = abs(int(width.replace("px", ""))) if width else 50
    h = abs(int(height.replace("px", ""))) if height else 50
    return [w, h]


def read_item_classes(item_id, item):
    el = item.find('a').find('div')
    classes = el.get('class')
    filtered_classes = ['item', 'inverse']
    filtered = [cls for cls in classes if cls not in filtered_classes]
    item_class = '.' + filtered[0]
    position_class = '.' + '.'.join(filtered)
    if 'rep-trink' in filtered:
        position_class = position_class.replace('.rep-item', '')
    item_styles = get_styles_by_class(item_class)
    position_styles = get_styles_by_class(position_class)
    image_url = extract_filename(item_styles.get('background'))
    if 'rep-trink' in filtered:
        rep_trink_styles = get_styles_by_class('.rep-trink')
        image_url = extract_filename(rep_trink_styles.get('background'))
    if image_url and image_url not in used_images:
        used_images.append(image_url)
    size = parse_size(position_styles, item_styles)
    item_position = position_styles and position_styles.get(
        "background-position")
    position = parse_position(item_position)
    save_image(item_id, image_url, position, size)
    return image_url, position, size


def parse_group_items(content):
    progress = Progress("Parsing group items")
    progress.start()

    items = []
    ids = []
    count = len(content)

    for i, item in enumerate(content):
        if not item.name:
            continue
        if item.name == 'h2':
            continue

        item_id = parse_item_id(item)
        if not item_id:
            continue

        name = parse_text_element(item, "item-title")
        description = parse_text_element(item, "pickup")
        quality = parse_number_element(item, "quality")
        content = parse_item_content(item)
        unlock = parse_text_element(item, "r-unlock")
        params = parse_items_params(item)

        image_url, position, size = read_item_classes(item_id, item)

        item = {
            "id": item_id,
            "name": name,
            "description": description,
            "quality": quality,
            "content": content,
            "unlock": unlock,
            "image_url": image_url,
            "position": position,
            "width": size[0],
            "height": size[1],
            **params,
        }
        items.append(item)
        ids.append(item_id)
        progress.update(item_id, i, count)

    progress.complete()
    return items, ids


def parse_group(content):
    if not content.name:
        return None
    children_length = len(content.find_all(recursive=False))
    if children_length <= 1:
        return None
    if content.find("h2"):
        name_content = content.find("h2").text
        match = re.match(r"^(.*?)\s*\((\d+)\)$", name_content)
        items, ids = parse_group_items(content)
        group = {
            "name": match.group(1) if match else name_content,
            "count": children_length - 1,
            "items": ids
        }
        return group, items
    return None


def format_item(item):
    formatted_item = " {\n"
    for key, value in item.items():
        item_content = dumps(
            value, ensure_ascii=False) if value is not None else 'null'
        formatted_item += f"        {key}: {item_content},\n"
    formatted_item += "      }"
    return formatted_item


def parse_html():
    with open(assets_html, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    main_div = soup.find("div", class_="main")
    if main_div:
        groups = []
        items = []
        for line in main_div.contents:
            result = parse_group(line)
            if result is not None:
                group, group_items = result
                if group is not None:
                    groups.append(group)
                if group_items is not None:
                    items.extend(group_items)
        os.makedirs(assets, exist_ok=True)
        return groups, items, used_images
