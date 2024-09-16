import json
from src.auto_publish import await_load_state
from .load_cookies import load_cookies
from .init_browser import init_browser
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
from src.log import logger


platform = "bjh"
url = "https://baijiahao.baidu.com/"


async def publish_to_bjh(video_file_path, title, description, tags, json_file_path):
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

        is_login2 = await page.locator(".author").is_visible()
        logger.info(f"Login status: {is_login2}")
        if not is_login2:
            try:
                logger.info("Not logged into the creation platform, starting login")
                await page.get_by_text("注册/登录百家号").click()
                await page.locator(".author").wait_for()
            except Exception as e:
                logger.error(f"Login failed: {e}")
                return

        await await_load_state(page)
        logger.info("Logged into the creation platform successfully")

        await save_cookies(cookie_file, page)

        # Go to publish page
        await page.locator("div.nav-switch-btn").first.click()
        await page.get_by_role("button", name="发布").hover()
        await page.locator("li.edit-video").click()
        await await_load_state(page)
        logger.info("Publish page opened successfully")

        logger.info(f"Video path: {video_file_path}")
        await page.locator("section.video-wrap input").set_input_files(video_file_path)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        await page.get_by_placeholder("请输入标题").clear()
        await page.get_by_placeholder("请输入标题").fill(title)
        logger.info("Title filled successfully")

        if not description:
            description = ""

        if not tags:
            tags = ""
        # Tags
        tags = tags.replace("#", "")
        await page.locator("div.form-inner-wrap input").last.fill(tags)
        await page.keyboard.press("Enter")
        logger.info("Tags filled successfully")

        # Description
        await page.locator("textarea").last.fill(description + title)
        logger.info("Description filled successfully")

        # Publish
        await page.pause()  # Remove this line or replace with appropriate wait strategy

        await page.get_by_role("button").first.click()
        logger.info("Video published successfully")
