import re
import os
import json
from bs4 import BeautifulSoup
from utils import extract_filename
from css import get_styles_by_class
from image import save_image
from globals import assets, assets_html, assets_items


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
    id = f"{prefix}-{value}"
    return id


def parse_item_content(item):
    el = item.find('span')
    lines = []
    for p in el.find_all('p', class_=False):
        if p.find_parent('ul') is None:
            lines.append(p.get_text())
    return "\n".join(lines)


def parse_items_params(item):
    lines = item.find('ul').find_all('p') if item.find('ul') else []
    type = None
    item_pool = None
    recharge_time = None
    for p in lines:
        text = p.get_text()
        if "Type" in text:
            type = text.split(': ')[-1]
        if "Pool" in text:
            item_pool = text.split(': ')[-1]
        if "Recharge" in text:
            recharge_time = text.split(': ')[-1]
    return {
        "type": type,
        "item_pool": item_pool,
        "recharge_time": recharge_time,
    }


def parse_position(str):
    if not str:
        return [0, 0]
    parts = str.split()
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


def read_item_classes(id, item):
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
    size = parse_size(position_styles, item_styles)
    item_position = position_styles and position_styles.get(
        "background-position")
    position = parse_position(item_position)
    save_image(id, image_url, position, size)


def parse_group_items(content):
    items = []
    for item in content:
        if not item.name:
            continue
        if item.name == 'h2':
            continue

        id = parse_item_id(item)
        if not id:
            continue

        name = parse_text_element(item, "item-title")
        description = parse_text_element(item, "pickup")
        quality = parse_number_element(item, "quality")
        content = parse_item_content(item)
        unlock = parse_text_element(item, "r-unlock")
        params = parse_items_params(item)

        read_item_classes(id, item)

        item = {
            "id": id,
            "name": name,
            "description": description,
            "quality": quality,
            "content": content,
            "unlock": unlock,
            **params,
        }
        items.append(item)
    return items


def parse_group(content):
    if not content.name:
        return None
    children_length = len(content.find_all(recursive=False))
    if children_length <= 1:
        return None
    if content.find("h2"):
        name_content = content.find("h2").text
        match = re.match(r"^(.*?)\s*\((\d+)\)$", name_content)
        items = parse_group_items(content)
        group = {
            "name": match.group(1) if match else name_content,
            "count": children_length - 1,
            "items": items
        }
        return group
    return None


def parse_html():
    with open(assets_html, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    main_div = soup.find("div", class_="main")
    if main_div:
        groups = []
        for line in main_div.contents:
            group = parse_group(line)
            if group is not None:
                groups.append(group)
        os.makedirs(assets, exist_ok=True)
        with open(assets_items, "w", encoding="utf-8") as json_file:
            json.dump(groups, json_file, ensure_ascii=False, indent=4)
    else:
        print("main div not found")
