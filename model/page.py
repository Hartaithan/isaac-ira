import os
import requests
from globals import url, assets, assets_html, load_timeout


def download_html():
    html_path = assets_html
    if not os.path.exists(html_path):
        response = requests.get(url, timeout=load_timeout)
        if response.status_code == 200:
            os.makedirs(assets, exist_ok=True)
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            print("html loaded")
        else:
            print(f"html load error {response.status_code}")
