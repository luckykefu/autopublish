import json
from src.auto_publish import await_load_state
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
from src.log import logger
from .load_cookies import load_cookies
from .init_browser import init_browser

logger.info(__file__)
platform = "vivo"
url = "https://kaixinkan.vivo.com.cn"


async def publish_to_vivo(video_file_path, title, description, tags, json_file_path):
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

        try:
            logger.info("Starting login process...")
            await page.get_by_role("button", name="创作者登录").click()
            await page.get_by_role("textbox", name="请输入手机号").fill(
                os.getenv("PHONE")
            )
            await page.wait_for_timeout(1000)
            await page.get_by_role("button", name="获取验证码").click()
            await page.wait_for_timeout(1000)
            await page.get_by_label("短信登录").locator("label span").nth(1).click()
            await page.get_by_role("button", name="发布内容").wait_for()

        except Exception as e:
            logger.error(f"Login failed: {e}")
            return

        await await_load_state(page)
        logger.info("Logged in to vivo successfully")
        await save_cookies(cookie_file, page)

        await page.get_by_role("button", name="发布内容").click()
        await await_load_state(page)
        logger.info("Successfully opened the publish page")

        await page.locator("div input[type='file']").set_input_files(video_file_path)
        await await_load_state(page)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        if not description:
            description = ""
        if not tags:
            tags = ""

        logger.info("Filling title and description...")
        await page.locator(".div").fill(title + "\n" + description + "\n" + tags)
        logger.info("Title and description filled successfully.")

        logger.info("Publishing video...")
        await page.pause()
        try:
            await page.get_by_role("button", name="发布").click()
            logger.info("Video published successfully.")
        except Exception as e:
            logger.error(f"Failed to publish video: {e}")
