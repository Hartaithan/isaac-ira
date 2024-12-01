import re


def extract_filename(value):
    match = re.search(r'[\w-]+\.\w+', value)
    return match.group(0) if match else None
