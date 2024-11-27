import re
import os
import requests
import numpy
from PIL import Image, ImageOps
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
        image = Image.open(assets_images + image_path)
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


def get_image_tilts(offset, width, height):
    tilts = {
        "top-tilt": [
            (offset, 0),
            (width - offset, 0),
            (width, height),
            (0, height)
        ],
        "top-left-tilt": [
            (offset, offset),
            (width, 0),
            (width - offset, height - offset),
            (0, height)
        ],
        "top-right-tilt": [
            (0, 0),
            (width - offset, offset),
            (width, height),
            (0, height - offset)
        ],
        "bottom-tilt": [
            (0, 0),
            (width, 0),
            (width - offset, height),
            (offset, height)
        ],
        "left-tilt": [
            (0, offset),
            (width, 0),
            (width, height),
            (0, height - offset)
        ],
        "right-tilt": [
            (0, 0),
            (width, offset),
            (width, height - offset),
            (0, height)
        ]
    }
    return tilts


def tilt_image(image, angle, path):
    width, height = image.size
    offset = width * angle

    tilts = get_image_tilts(offset, width, height)

    for name, target in tilts.items():
        source = [(0, 0), (width, 0), (width, height), (0, height)]
        coeffs = find_coeffs(source, target)
        transformed_image = image.transform(
            (width, height), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
        output_path = f'{path}/{angle * 100}-{name}.png'
        transformed_image.save(output_path)


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
