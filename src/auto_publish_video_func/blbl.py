import json
from ..auto_publish import await_load_state
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
from src.log import get_logger

logger = get_logger(__name__)
from .load_cookies import load_cookies
from .init_browser import init_browser


platform = "blbl"
url = "https://www.bilibili.com/"


async def publish_to_blbl(video_file_path, title, description, tags, json_file_path):
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return

    async with async_playwright() as p:

        # Initialize the browser
        try:
            # Launch persistent browser context
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

        is_login2 = await page.get_by_text("登录", exact=True).is_visible()
        logger.info(f"Login status: {is_login2}")
        if is_login2:
            try:
                logger.info("Not logged into the creation platform, starting login")
                await page.get_by_text("登录", exact=True).click()
                await page.get_by_text("短信登录").click()
                await page.get_by_placeholder("请输入手机号").fill(os.getenv("PHONE"))
                await page.get_by_text("获取验证码").click()
                await page.wait_for_selector("li.header-avatar-wrap picture img")
            except Exception as e:
                logger.error(f"Login failed: {e}")
                return

        await await_load_state(page)
        logger.info("Logged into the creation platform successfully")
        await save_cookies(cookie_file, page)

        # Publish video
        async with page.expect_popup() as p1_info:
            await page.get_by_role("link", name="投稿", exact=True).click()
        page1 = await p1_info.value
        await await_load_state(page1)
        logger.info("Publish page opened successfully")

        logger.info(f"Video path: {video_file_path}")
        await page1.locator("div.upload-wrp input").set_input_files(video_file_path)
        if await page1.get_by_text("知道了", exact=True).is_visible():
            await page1.get_by_text("知道了", exact=True).click()
        await await_load_state(page1)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        await page1.locator("input.input-val").first.clear()
        await page1.locator("input.input-val").first.fill(title)
        logger.info("Title filled successfully")

        # Tags
        if not tags:
            tags = ""
        if not description:
            description = ""

        tags = tags.split("#")
        for tag in tags:
            await page1.locator("div.tag-input-wrp input.input-val").first.fill(tag)
            await page1.keyboard.press("Enter")
            await page1.wait_for_timeout(1000)
        logger.info("Tags filled successfully")

        # Description
        await page1.locator(".ql-editor > p").first.fill(description)
        logger.info("Description filled successfully")

        # Publish
        logger.info("Publishing video...")
        await page1.pause()  # Remove this line or replace with appropriate wait strategy
        await page1.get_by_text("立即投稿").click()
        logger.info("Video published successfully")


# Example run
if __name__ == "__main__":
    import asyncio

    asyncio.run(
        publish_to_blbl(
            "path/to/video.mp4",
            "My Title",
            "This is a description.",
            "tag1, tag2",
            "path/to/json.json",
        )
    )
