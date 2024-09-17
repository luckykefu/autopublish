import json
from src.log import get_logger
logger = get_logger(__name__)

def get_title_description_tags(json_file_path):
    """
    Get title, description and tags from json file.
    """
    logger.info(f"Getting title, description and tags from {json_file_path}")
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data["title"]
    description = data["description"]
    tags = data["tags"].replace(" ", "")
    logger.info(f"Title: {title}")
    logger.info(f"Description: {description}")
    logger.info(f"Tags: {tags}")

    return title, description, tags


