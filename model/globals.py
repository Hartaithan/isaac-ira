import os

url = "https://tboi.com"
assets = os.path.join("model", "assets")
pre_dataset = os.path.join("model", "pre-dataset")
dataset = os.path.join("model", "dataset")

url_css = f"{url}/assets/main.css"
assets_css = os.path.join(assets, "main.css")

assets_images = os.path.join(assets, "images")
assets_cropped = os.path.join(assets, "cropped")

assets_html = os.path.join(assets, "index.html")

assets_items = os.path.join(assets, "items.json")

load_timeout = 30
