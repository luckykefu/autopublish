from ..auto_publish import await_load_state

from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
import json
from src.log import get_logger

logger = get_logger(__name__)
from .load_cookies import load_cookies
from .init_browser import init_browser

# Get current script name

platform = "zhihu"
url = "https://www.zhihu.com/"


async def publish_to_zhihu(video_file_path, title, description, tags, json_file_path):
    """
    Publish a video to Zhihu.
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
            return None

        cookie_file = f"cookies\\{platform}.json"

        # Load cookies
        if os.path.exists(cookie_file):
            try:
                await load_cookies(browser, cookie_file)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from cookies file: {e}")
            except Exception as e:
                logger.error(f"Failed to load cookies: {e}")

        # Open Zhihu url
        page = await browser.new_page()
        await page.goto(url)
        await await_load_state(page)
        logger.info("Zhihu url opened successfully")

        is_login2 = await page.get_by_placeholder("手机号").is_visible()
        logger.info(f"Login status: {is_login2}")
        if is_login2:
            try:
                logger.info("Not logged in to Zhihu, starting login")
                await page.get_by_role("button", name="密码登录").click()
                await page.get_by_placeholder("手机号或邮箱").fill(os.getenv("PHONE"))
                await page.get_by_placeholder("密码").fill(os.getenv("ZHIHU_PASSWORD"))
                await page.get_by_role("button", name="登录", exact=True).click()
                await page.get_by_role("button", name="发视频").wait_for()
            except Exception as e:
                logger.error(e)
                return

        await await_load_state(page)
        logger.info("Login successful")
        await save_cookies(cookie_file, page)

        async with page.expect_popup() as p1_info:
            await page.get_by_role("button", name="发视频").click()
        page1 = await p1_info.value
        await await_load_state(page1)

        await page1.locator("div input[type='file']").set_input_files(video_file_path)
        logger.info(f"Video file set to {video_file_path}")
        await await_load_state(page1)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]
            logger.info(f"Title set to {title}")

        await page1.get_by_placeholder("输入视频标题").fill(title)
        logger.info(f"Title set to {title}")

        if not description:
            description = ""
        if not tags:
            tags = ""

        await page1.get_by_placeholder("填写视频简介，让更多人找到你的视频").fill(
            description + "\n" + tags
        )
        logger.info(f"Description and tags set to {description} {tags}")

        await page1.get_by_text("选择领域").click()
        await page1.get_by_role("option", name="生活").click()
        await page1.get_by_text("选择领域").click()
        await page1.get_by_role("option", name="兴趣").click()
        logger.info("Categories set to 生活 兴趣")

        # await page1.get_by_role("button", name="​ 绑定话题（至少添加一个）").click()
        # await page1.locator("#Popover15-toggle").fill(title)
        # await page1.locator("div.Menu-item.is-active").click()

        await page1.get_by_text("原创").click()
        logger.info("License set to 原创")

        logger.info("Verifying video information")
        await page.pause()

        await page1.get_by_role("button", name="发布视频").click()
        logger.info("Video published successfully")
