import re
import os
import requests
import numpy
from PIL import Image, ImageOps, ImageEnhance
from globals import url, assets_css, assets_images, assets_cropped, load_timeout, pre_dataset


def download_all_images():
    # get all images
    with open(assets_css, "r", encoding="utf-8") as file:
        css_content = file.read()
    pattern = r'background:\s*url\((["\']?.+?["\']?)\)'
    image_urls = re.findall(pattern, css_content)
    image_urls = [url.strip('"').strip("'") for url in image_urls]
    # download all images
    os.makedirs(assets_images, exist_ok=True)
    for i, image_url in enumerate(image_urls):
        image_url = url + image_url.replace("..", "")
        filename = image_url.split("/")[-1]
        path = f"{assets_images}/{filename}"
        if not os.path.exists(path):
            response = requests.get(image_url, timeout=load_timeout)
            if response.status_code == 200:
                with open(path, "wb") as file:
                    file.write(response.content)
                print(f"image {path} loaded")
            else:
                print(f"image {path} load error {response.status_code}")


def save_image(id, image_path, position, size):
    try:
        path = os.path.join(assets_images, image_path)
        image = Image.open(path)
        x, y = position
        width, height = size
        box = (x, y, x + width, y + height)
        cropped_image = image.crop(box)
        output = assets_cropped
        os.makedirs(output, exist_ok=True)
        filename = f"{id}.png"
        output_path = os.path.join(output, filename)
        cropped_image.save(output_path)
    except Exception as e:
        print(f"save image error: {e}")


def resize_image(image, width=None, height=None):
    method = Image.Resampling.LANCZOS
    image = ImageOps.contain(image, (width, height), method=method)
    resized = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = (width - image.width) // 2
    y = (height - image.height) // 2
    resized.paste(image, (x, y))
    return resized


def find_coeffs(source, target):
    matrix = []
    for s, t in zip(source, target):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(source).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def get_image_tilts(offset, w, h):
    top = [(offset, 0), (w - offset, 0), (w, h), (0, h)]
    top_left = [(offset, offset), (w, 0), (w - offset, h - offset), (0, h)]
    top_right = [(0, 0), (w - offset, offset), (w, h), (0, h - offset)]
    bottom = [(0, 0), (w, 0), (w - offset, h), (offset, h)]
    left = [(0, offset), (w, 0), (w, h), (0, h - offset)]
    right = [(0, 0), (w, offset), (w, h - offset), (0, h)]
    tilts = {
        "tilt-top": top,
        "tilt-top-left": top_left,
        "tilt-top-right": top_right,
        "tilt-bottom": bottom,
        "tilt-left": left,
        "tilt-right": right
    }
    return tilts


def tilt_image(image, angle, path):
    width, height = image.size
    offset = width * angle

    tilts = get_image_tilts(offset, width, height)

    for name, target in tilts.items():
        source = [(0, 0), (width, 0), (width, height), (0, height)]
        coeffs = find_coeffs(source, target)
        transformed = image.transform(
            (width, height), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
        output_path = f'{path}/{name}-[{angle * 100}].png'
        transformed.save(output_path)


def change_brightness(image, brightness, path):
    enhancer = ImageEnhance.Brightness(image)
    transformed = enhancer.enhance(brightness)
    output_path = f'{path}/brightness-[{brightness}].png'
    transformed.save(output_path)


def prepare_images():
    for filename in os.listdir(assets_cropped):
        image_path = os.path.join(assets_cropped, filename)
        image = Image.open(image_path)
        image = resize_image(image, 224, 224)

        output_folder = f"{pre_dataset}/{filename.replace('.png', '')}"
        os.makedirs(output_folder, exist_ok=True)
        image.save(f'{output_folder}/original.png')

        tilt_image(image, 0.05, output_folder)
        tilt_image(image, 0.10, output_folder)
        tilt_image(image, 0.15, output_folder)

        change_brightness(image, 0.25, output_folder)
        change_brightness(image, 0.5, output_folder)
        change_brightness(image, 0.75, output_folder)
        change_brightness(image, 1.25, output_folder)
        change_brightness(image, 1.5, output_folder)
