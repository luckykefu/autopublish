from ..auto_publish import await_load_state
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
from src.log import get_logger

logger = get_logger(__name__)
import json
from .load_cookies import load_cookies
from .init_browser import init_browser


platform = "weibo"
url = "https://weibo.com/upload/channel"


async def publish_to_weibo(video_file_path, title, description, tags, json_file_path):
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return
    async with async_playwright() as p:
        try:
            browser = await init_browser(p)
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return

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

        is_login2 = await page.get_by_role("button", name="立即 登录").is_visible()
        logger.info(f"Login status: {is_login2}")
        if is_login2:
            try:
                logger.info("Not logged in to Weibo, starting login")
                await page.get_by_role("button", name="立即 登录").click()
                await page.get_by_role("button", name="上传视频").wait_for()
            except Exception as e:
                logger.error(f"Login failed: {e}")
                return
        await await_load_state(page)
        logger.info("Logged in to Weibo successfully")
        await save_cookies(cookie_file, page)

        logger.info("Video path:", video_file_path)
        page.once(
            "filechooser", lambda file_chooser: file_chooser.set_files(video_file_path)
        )
        await page.get_by_role("button", name="上传视频").click()
        await await_load_state(page)

        logger.info("Selected original content")
        await page.get_by_text("原创").click()

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        await page.locator("input[type='text']").first.fill(title)
        logger.info("Filled title successfully")

        if description is None:
            description = ""
        if tags is None:
            tags = ""

        await page.locator("textarea").first.fill(description + "\n" + tags)
        logger.info("Filled description successfully")

        logger.info("Pausing before publishing...")
        await page.pause()

        await page.wait_for_timeout(3000)
        logger.info("Publishing...")
        await page.get_by_role("button", name="发布").click()
        logger.info("Published successfully")
