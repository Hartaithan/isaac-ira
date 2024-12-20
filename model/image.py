import re
import os
import requests
import numpy
import pillow_avif  # pylint: disable=W0611
from PIL import Image, ImageOps, ImageEnhance
from globals import load_timeout, pre_dataset, background
from globals import url, assets_css, assets_images, assets_cropped, assets_used


def download_all_images():
    # get all images
    with open(assets_css, "r", encoding="utf-8") as file:
        css_content = file.read()
    pattern = r'background:\s*url\((["\']?.+?["\']?)\)'
    image_urls = re.findall(pattern, css_content)
    image_urls = [url.strip('"').strip("'") for url in image_urls]
    # download all images
    os.makedirs(assets_images, exist_ok=True)
    for _i, image_url in enumerate(image_urls):
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


def save_image(name, image_path, position, size):
    try:
        path = os.path.join(assets_images, image_path)
        image = Image.open(path)
        x, y = position
        width, height = size
        box = (x, y, x + width, y + height)
        cropped_image = image.crop(box)
        os.makedirs(assets_cropped, exist_ok=True)
        filename = f"{name}.png"
        output_path = os.path.join(assets_cropped, filename)
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


def add_background(image):
    transformed = Image.new('RGBA', image.size, background)
    transformed.paste(image, mask=image)
    return transformed


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
            (width, height), Image.Transform.PERSPECTIVE, coeffs, resample=Image.Resampling.BICUBIC)
        output_path = f'{path}/{name}-[{angle}].png'
        transformed = add_background(transformed)
        transformed.save(output_path)


def change_brightness(image, brightness, path):
    enhancer = ImageEnhance.Brightness(image)
    transformed = enhancer.enhance(brightness)
    output_path = f'{path}/brightness-[{brightness}].png'
    transformed.save(output_path)


def rotate_image(image, rotate, path):
    transformed = image.rotate(rotate)
    output_path = f'{path}/rotate-[{rotate}].png'
    transformed = add_background(transformed)
    transformed.save(output_path)


def scale_image(image, scale, filename, path):
    orig_width, orig_height = image.size
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    new_aspect_ratio = new_width / new_height
    image_bg = image.getpixel((0, 0))
    if orig_width / orig_height > new_aspect_ratio:
        new_width = int(new_height * orig_width / orig_height)
    else:
        new_height = int(new_width * orig_height / orig_width)
    transformed = Image.new('RGB', (new_width, new_height), image_bg)
    transformed.paste(image, ((new_width - orig_width) //
                              2, (new_height - orig_height) // 2))
    transformed = transformed.resize((orig_width, orig_height))
    new_filename = filename.replace('.png', '')
    output_path = f'{path}/scale-[{scale}]-{new_filename}.png'
    transformed.save(output_path)


def prepare_images():
    for filename in os.listdir(assets_cropped):
        if filename == '.DS_Store':
            continue
        image_path = os.path.join(assets_cropped, filename)
        image = Image.open(image_path)
        image = resize_image(image, 224, 224)
        image = add_background(image)

        output_folder = f"{pre_dataset}/{filename.replace('.png', '')}"
        os.makedirs(output_folder, exist_ok=True)
        image.save(f'{output_folder}/original.png')

        tilt_image(image, 0.05, output_folder)
        tilt_image(image, 0.075, output_folder)
        tilt_image(image, 0.10, output_folder)
        tilt_image(image, 0.125, output_folder)
        tilt_image(image, 0.15, output_folder)

        change_brightness(image, 0.25, output_folder)
        change_brightness(image, 0.5, output_folder)
        change_brightness(image, 0.75, output_folder)
        change_brightness(image, 1.25, output_folder)
        change_brightness(image, 1.5, output_folder)

        rotate_image(image, -10, output_folder)
        rotate_image(image, -5, output_folder)
        rotate_image(image, -3, output_folder)
        rotate_image(image, 3, output_folder)
        rotate_image(image, 5, output_folder)
        rotate_image(image, 10, output_folder)


def scale_predataset():
    for folder in os.listdir(pre_dataset):
        if folder == '.DS_Store':
            continue
        subfolder_path = os.path.join(pre_dataset, folder)
        for filename in os.listdir(subfolder_path):
            if filename == '.DS_Store':
                continue
            image_path = os.path.join(pre_dataset, folder, filename)
            image = Image.open(image_path)
            scale_image(image, 1.1, filename, subfolder_path)
            scale_image(image, 1.2, filename, subfolder_path)
            scale_image(image, 1.3, filename, subfolder_path)


def save_used_images(images: list[str]):
    os.makedirs(assets_used, exist_ok=True)
    for filename in images:
        image_path = os.path.join(assets_images, filename)
        if not os.path.exists(image_path):
            print(f"used image {image_path} does not exist")
            continue
        image = Image.open(image_path)
        output_path = os.path.join(assets_used, filename)
        output_path = output_path.replace('.png', '.avif')
        image.save(output_path, format='avif', quality=50)
