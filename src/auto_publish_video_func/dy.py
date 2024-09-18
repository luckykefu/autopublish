import json
from .load_cookies import load_cookies
from .init_browser import init_browser
from ..auto_publish import await_load_state
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
from ..log import get_logger

logger = get_logger(__name__)


platform = "dy"
url = "https://creator.douyin.com"


async def publish_to_dy(video_file_path, title, description, tags, json_file_path):
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return
    async with async_playwright() as p:
        # Initialize the browser
        try:
            browser = await init_browser(p)
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return None
        # Cookies file path
        cookie_file = f"cookies\\{platform}.json"

        # Load cookies
        if os.path.exists(cookie_file):
            try:
                await load_cookies(browser, cookie_file)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from cookies file: {e}")
            except Exception as e:
                logger.error(f"Failed to load cookies: {e}")

        page = await browser.new_page()
        await page.goto(url)
        await await_load_state(page)

        is_login2 = await page.get_by_text("扫码登录").is_visible()
        logger.info(f"logging status: {is_login2}")
        if not is_login2:
            try:
                logger.info("Not logged into the creation platform, starting login")
                await page.get_by_text("发布视频").wait_for()
            except Exception as e:
                logger.error(e)
                return

        await await_load_state(page)
        logger.info("Logged into the creation platform successfully")

        await save_cookies(cookie_file, page)

        await page.get_by_text("发布视频").click()
        await await_load_state(page)

        # Upload video
        logger.info(f"Video path: {video_file_path}")
        await page.locator("input").set_input_files(video_file_path)
        await await_load_state(page)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        await page.locator("div.editor-kit-editor-container input").fill(title)
        logger.info("Title filled successfully")

        if not description:
            description = ""
        if not tags:
            tags = ""

        # Description
        await page.locator(".zone-container").fill(
            description + "\n" + tags.replace(" ", "").replace("#", "  #")
        )
        logger.info("Description filled successfully")

        # Simulate pressing Enter key
        await page.keyboard.press("Enter")
        await await_load_state(page)

        logger.info("Waiting for video to be uploaded...")
        await page.pause()

        await page.get_by_role("button", name="发布", exact=True).click()
        logger.info("Video published successfully")
