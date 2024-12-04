from css import download_css
from image import download_all_images, prepare_images, scale_predataset
from page import download_html
from parse import parse_html
from group import group_dataset

download_css()
download_all_images()
download_html()
parse_html()
prepare_images()
scale_predataset()
group_dataset()
