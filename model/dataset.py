from css import download_css
from image import download_all_images, prepare_images, scale_dataset, save_used_images
from page import download_html
from parse import parse_html, save_groups, save_items
from group import group_dataset

download_css()
download_all_images()
download_html()
groups, items, used_images = parse_html()
save_groups(groups)
save_items(items)
save_used_images(used_images)
prepare_images()
scale_dataset()
group_dataset()
