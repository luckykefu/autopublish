from ..log import get_logger

logger = get_logger(__name__)
import json


async def load_cookies(browser, cookie_file):
    with open(cookie_file, "r") as f:
        logger.info("Loading cookies...")
        cookies = json.load(f)
        if isinstance(cookies, list):
            await browser.add_cookies(cookies)
            logger.info("Cookies loaded successfully.")
        else:
            logger.error("Invalid cookies format. Expected a list of cookies.")
