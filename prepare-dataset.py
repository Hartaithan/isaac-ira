import re
import os
import requests

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
