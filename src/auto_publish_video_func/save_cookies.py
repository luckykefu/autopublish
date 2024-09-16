import json
import os
from src.log import logger


async def save_cookies(cookie_file, page):
    # Extract the directory path from the full file path
    directory = os.path.dirname(cookie_file)
    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(directory):
        logger.info(f"Creating directory: {directory}")
        os.makedirs(directory)

    logger.info("save cookies")
    
    cookies = await page.context.cookies()
    with open(cookie_file, "w") as f:
        json.dump(cookies, f, indent=4)
        
    logger.info("save cookies success")
