from css import download_css
from image import download_all_images, prepare_images, create_sprite_sheet
from page import download_html
from parse import parse_html
from items import save_groups, save_items
from dataset import group_dataset, scale_dataset

download_css()
download_all_images()
download_html()
groups, items, used_images = parse_html()
positioned_items = create_sprite_sheet(items)
save_groups(groups)
save_items(positioned_items)
prepare_images()
scale_dataset()
group_dataset()
