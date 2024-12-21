import os
import requests
from globals import url, assets, assets_html, load_timeout
from progress import Progress


def download_html():
    progress = Progress("Downloading HTML")
    progress.start()
    html_path = assets_html
    if not os.path.exists(html_path):
        response = requests.get(url, timeout=load_timeout)
        if response.status_code == 200:
            os.makedirs(assets, exist_ok=True)
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            progress.complete()
        else:
            progress.complete(f"error {response.status_code}")
    else:
        progress.complete()
