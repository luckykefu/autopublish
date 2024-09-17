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


platform = "sph"
url = "https://channels.weixin.qq.com/platform/post/create"


async def publish_to_sph(video_file_path, title, description, tags, json_file_path):
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return
    async with async_playwright() as p:
        # Initialize the browser
        try:
            # Initialize browser context
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
            await page.wait_for_timeout(3000)
            is_logged_in = await page.locator("img.avatar").is_visible()
            if not is_logged_in:
                try:
                    logger.info("Not logged in to WeChat, starting login")
                    await page.wait_for_selector("img.avatar")
                except Exception as e:
                    logger.error(f"Failed to wait for login element: {e}")
                    return

            await await_load_state(page)
            logger.info("Logged in to WeChat successfully")
            await save_cookies(cookie_file, page)

            logger.info(f"Video path: {video_file_path}")
            await page.locator('input[type="file"]').set_input_files(video_file_path)
            await await_load_state(page)

            if json_file_path:
                title, description, tags = get_title_description_tags(json_file_path)

            if not title:
                title = os.path.splitext(os.path.basename(video_file_path))[0]

            if not description:
                description = ""

            if not tags:
                tags = ""

            await page.locator(".input-editor").fill(
                description + "\n" + tags.replace(" ", "")
            )
            logger.info("Filled description successfully")

            await page.locator("div.post-short-title-wrap input[type='text']").fill(
                title
            )
            logger.info("Filled title successfully")

            # Publish
            logger.info("Publishing...")
            await page.pause()
            await page.get_by_role("button", name="Publish").click()
            logger.info("Published successfully")
        except Exception as e:
            logger.error(f"An error occurred during publishing: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        publish_to_sph(
            video_file_path=r"D:\Videos\041.mp4",
            title=None,
            description=None,
            tags=None,
            json_file_path=None,
        )
    )
