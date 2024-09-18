import json
import os
from .log import get_logger

logger = get_logger(__name__)


def save_title_description_tags(title, description, tags, output_dir="temp"):
    logger.info(f"Saving title, description, and tags")

    os.makedirs(output_dir, exist_ok=True)
    json_file_path = os.path.join(output_dir, title + ".json")

    data = {"title": title, "description": description, "tags": tags}
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved title, description, and tags to {json_file_path}")
    return json_file_path


async def await_load_state(page):
    logger.info("Waiting for page to load...")
    await page.wait_for_load_state("load")
    # await page.wait_for_load_state("domcontentloaded")
    # await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(5000)
    logger.info("Page loaded")


if __name__ == "__main__":
    json_file_path = "test.json"
    title = "Test Title"
    description = "Test Description"
    tags = ["test", "tags"]
    save_title_description_tags(json_file_path, title, description, tags)
