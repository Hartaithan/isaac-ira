import os

root = "model"

url = "https://tboi.com"

assets = os.path.join(root, "assets")
pre_dataset = os.path.join(root, "pre-dataset")
dataset = os.path.join(root, "dataset")

url_css = f"{url}/assets/main.css"
assets_css = os.path.join(assets, "main.css")

assets_images = os.path.join(assets, "images")
assets_cropped = os.path.join(assets, "cropped")
assets_used = os.path.join(assets, "used")

assets_html = os.path.join(assets, "index.html")
assets_groups = os.path.join(assets, "groups.ts")
assets_items = os.path.join(assets, "items.ts")
assets_classes = os.path.join(assets, "classes.ts")

background = (77, 44, 37, 255)

load_timeout = 30
