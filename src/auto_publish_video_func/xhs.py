import json
import os
from playwright.async_api import async_playwright
from ..auto_publish import await_load_state
from src.log import get_logger

logger = get_logger(__name__)
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from .load_cookies import load_cookies
from .init_browser import init_browser

# Get current script name

platform = "xhs"  # Fixed typo 'platfrom' to 'platform'
url = "https://creator.xiaohongshu.com/"


async def publish_to_xhs(video_file_path, title, description, tags, json_file_path):
    """
    Publish a video to Xiaohongshu.
    :param video_file_path: Path to the video file.
    :param title: Title of the post.
    :param description: Description of the post.
    :param tags: Tags for the post.
    :param json_file_path: Path to the JSON file containing details.
    :return:
    """
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return

    async with async_playwright() as p:
        # Initialize browser
        try:
            browser = await init_browser(p)
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

        cookie_file = f"cookies\\{platform}.json"
        # Load cookies
        if os.path.exists(cookie_file):
            try:
                await load_cookies(browser, cookie_file)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from cookies file: {e}")
            except Exception as e:
                logger.error(f"Failed to load cookies: {e}")

        # Open Xiaohongshu creator platform
        page = await browser.new_page()
        await page.goto(url)
        await await_load_state(page)

        # Login to the creation service platform
        is_logged_in = await page.locator("a.btn").is_visible()
        logger.info("Is logged in to creation service platform:", is_logged_in)
        if not is_logged_in:
            try:
                logger.info("Starting login")
                await page.get_by_placeholder("手机号").fill(os.getenv("PHONE"))
                await page.get_by_text("发送验证码").click()
                await page.wait_for_selector("a.btn")
            except Exception as e:
                logger.error(f"Failed to login: {e}")
                raise

        await await_load_state(page)
        logger.info("Logged in to creation service platform successfully")

        # Save cookies
        await save_cookies(cookie_file, page)

        # Upload video
        await page.get_by_text("发布笔记", exact=True).click()
        await await_load_state(page)

        logger.info("Video path:", video_file_path)
        await page.locator("div.drag-over input").set_input_files(video_file_path)
        await await_load_state(page)

        # Get title, description, and tags from JSON file
        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]

        # Fill in the title
        await page.locator("div.titleInput input").first.fill(title)
        logger.info("Title filled successfully")

        # Fill in the description
        if description is None:
            description = ""
        if tags is None:
            tags = ""
        await page.locator("#post-textarea").fill(description + "\n" + tags)
        logger.info("Description filled successfully")

        # Press Enter
        await page.locator("#post-textarea").press("Enter")
        await page.keyboard.press("Enter")

        # Publish
        logger.info("Publishing...")
        await page.pause()

        await page.get_by_role("button", name="发布").click()
        logger.info("Published successfully")
