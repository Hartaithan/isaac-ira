import re
import os
import requests
import json
from bs4 import BeautifulSoup


url = "https://tboi.com"
assets = "assets"
styles_url = f"{url}/{assets}/main.css"
load_timeout = 30


# loading css
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
    print("css already loaded")


# get all images
with open(f"{assets}/main.css", "r", encoding="utf-8") as file:
    css_content = file.read()
image_urls = re.findall(r'background:\s*url\((["\']?.+?["\']?)\)', css_content)
image_urls = [url.strip('"').strip("'") for url in image_urls]
print("list of images")
print(image_urls)


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
    else:
        print(f"image {path} already loaded")


# upload html
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
else:
    print("html already loaded")


# parse item groups
def parse_item_group(content):
    # skip not valid groups
    if not content.name:
        return None
    children_length = len(content.find_all(recursive=False))
    if children_length <= 1:
        return None
    if content.find("h2"):
        name_content = content.find("h2").text
        match = re.match(r"^(.*?)\s*\((\d+)\)$", name_content)
        group = {
            "name": match.group(1) if match else name_content,
            "count": children_length - 1,
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
    print(groups)
    os.makedirs("assets", exist_ok=True)
    with open("assets/items.json", "w", encoding="utf-8") as json_file:
        json.dump(groups, json_file, ensure_ascii=False, indent=4)
else:
    print("main div not found")
