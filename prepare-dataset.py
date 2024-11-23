import re
import os
import requests
import json
from bs4 import BeautifulSoup

url = "https://tboi.com"
assets = "assets"
styles_url = f"{url}/{assets}/main.css"
load_timeout = 30


# download css
path = f"{assets}/main.css"
if not os.path.exists(path):
    response = requests.get(styles_url, timeout=load_timeout)
    if response.status_code == 200:
        css_content = response.text
        os.makedirs("assets", exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(css_content)
        print("css loaded")
    else:
        print(f"css load error {response.status_code}")
else:
    with open(path, "r", encoding="utf-8") as file:
        css_content = file.read()


# get all images
with open(f"{assets}/main.css", "r", encoding="utf-8") as file:
    css_content = file.read()
image_urls = re.findall(r'background:\s*url\((["\']?.+?["\']?)\)', css_content)
image_urls = [url.strip('"').strip("'") for url in image_urls]


# download all images
os.makedirs("assets/images", exist_ok=True)
for i, image_url in enumerate(image_urls):
    image_url = url + image_url.replace("..", "")
    filename = image_url.split("/")[-1]
    path = f"{assets}/images/{filename}"
    if not os.path.exists(path):
        response = requests.get(image_url, timeout=load_timeout)
        if response.status_code == 200:
            with open(path, "wb") as file:
                file.write(response.content)
            print(f"image {path} loaded")
        else:
            print(f"image {path} load error {response.status_code}")


# download html
html_path = f"{assets}/index.html"
if not os.path.exists(html_path):
    response = requests.get(url, timeout=load_timeout)
    if response.status_code == 200:
        os.makedirs("assets", exist_ok=True)
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print("html loaded")
    else:
        print(f"html load error {response.status_code}")


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


def get_item_content(item):
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


def get_item_id(item):
    id = item.get('data-tid')
    if id is not None:
        try:
            id = int(id)
        except ValueError:
            id = None
    return id


def get_styles_for_class(class_name):
    class_regex = re.compile(
        rf"{re.escape(class_name)}\s*\{{(.*?)\}}",
        re.DOTALL
    )
    match = class_regex.search(css_content)
    if not match:
        return None
    styles_text = match.group(1)
    styles = {}
    for style_match in re.finditer(r"([\w-]+)\s*:\s*([^;]+);?", styles_text):
        property_name = style_match.group(1).strip()
        value = style_match.group(2).strip()
        styles[property_name] = value
    return styles


def read_item_classes(item):
    el = item.find('a').find('div')
    classes = el.get('class')
    filtered_classes = ['item', 'inverse']
    filtered = [cls for cls in classes if cls not in filtered_classes]
    item_class = '.' + '.'.join(filtered)
    if 'rep-trink' in filtered:
        item_class = item_class.replace('.rep-item', '')
    item_styles = get_styles_for_class(item_class)
    return item_styles


def parse_group_items(content):
    items = []
    for item in content:
        if not item.name:
            continue
        if item.name == 'h2':
            continue

        id = get_item_id(item)
        name = parse_text_element(item, "item-title")
        description = parse_text_element(item, "pickup")
        quality = parse_number_element(item, "quality")
        content = get_item_content(item)
        unlock = parse_text_element(item, "r-unlock")
        params = parse_items_params(item)

        read_item_classes(item)

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


def parse_item_group(content):
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


# parse html
with open(html_path, "r", encoding="utf-8") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "html.parser")
main_div = soup.find("div", class_="main")
if main_div:
    groups = []
    for line in main_div.contents:
        group = parse_item_group(line)
        if group is not None:
            groups.append(group)
    os.makedirs("assets", exist_ok=True)
    with open("assets/items.json", "w", encoding="utf-8") as json_file:
        json.dump(groups, json_file, ensure_ascii=False, indent=4)
else:
    print("main div not found")
