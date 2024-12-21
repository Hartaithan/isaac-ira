import re
import os
import requests
from globals import assets, assets_css, url_css, load_timeout
from progress import Progress


def download_css():
    progress = Progress("Downloading CSS")
    progress.start()
    if not os.path.exists(assets_css):
        response = requests.get(url_css, timeout=load_timeout)
        if response.status_code == 200:
            css_content = response.text
            os.makedirs(assets, exist_ok=True)
            with open(assets_css, "w", encoding="utf-8") as file:
                file.write(css_content)
            progress.complete()
        else:
            progress.complete(f"error {response.status_code}")
    else:
        with open(assets_css, "r", encoding="utf-8") as file:
            css_content = file.read()
        progress.complete()


def get_styles_by_class(class_name):
    with open(assets_css, "r", encoding="utf-8") as file:
        css_content = file.read()
    pattern = rf"{re.escape(class_name)}\s*\{{(.*?)\}}"
    regex = re.compile(pattern, re.DOTALL)
    match = regex.search(css_content)
    if not match:
        return None
    styles_text = match.group(1)
    styles = {}
    for style_match in re.finditer(r"([\w-]+)\s*:\s*([^;]+);?", styles_text):
        property_name = style_match.group(1).strip()
        value = style_match.group(2).strip()
        styles[property_name] = value
    return styles
