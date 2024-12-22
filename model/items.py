from progress import Progress
from parse import format_item
from globals import assets_groups, assets_items


def save_groups(groups):
    progress = Progress("Generating groups list")
    progress.start()
    content = "import { ItemGroup } from \"@/model/item\";\n\n"
    content += "export const groups: ItemGroup[] = [\n"
    content += ",\n".join([
        "  {\n" +
        f"    name: \"{group['name']}\",\n" +
        f"    count: {group['count']},\n" +
        f"    items: {group['items']}\n" +
        "  }"
        for group in groups
    ])
    content += "\n];\n"
    with open(assets_groups, "w", encoding="utf-8") as ts_file:
        ts_file.write(content)
    progress.complete()


def save_items(items):
    progress = Progress("Generating items list")
    progress.start()
    content = "import { Item } from \"@/model/item\";\n\n"
    content += "export const items: Record<string, Item> = {\n"
    content += ",\n".join([
        f"  \"{item['id']}\": " + format_item(item)
        for item in items
    ])
    content += "\n};\n"
    with open(assets_items, "w", encoding="utf-8") as ts_file:
        ts_file.write(content)
    progress.complete()
