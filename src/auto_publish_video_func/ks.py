from ..auto_publish import await_load_state
from .get_title_description_tags import get_title_description_tags
from .save_cookies import save_cookies
from playwright.async_api import async_playwright
import os
import json
import re
from src.log import get_logger

logger = get_logger(__name__)
from .init_browser import init_browser
from .load_cookies import load_cookies


platform = "ks"
url = "https://cp.kuaishou.com/article/publish/video"


async def publish_to_ks(video_file_path, title, description, tags, json_file_path):
    if video_file_path is None or not os.path.exists(video_file_path):
        logger.error(f"Video file not found: {video_file_path}")
        return
    async with async_playwright() as p:
        try:
            # 初始化浏览器上下文
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

        page = await browser.new_page()
        await page.goto(url)
        await await_load_state(page)

        is_login2 = await page.locator("a.login").is_visible()
        logger.info(f"Login status: {is_login2}")
        if is_login2:
            try:
                logger.info("未登录创作服务平台, 开始登录")
                await page.locator("a.login").click()
                await page.get_by_text("验证码登录").click()
                await page.get_by_placeholder("请输入手机号").fill(os.getenv("PHONE"))
                await page.locator("div").filter(
                    has_text=re.compile(r"^获取验证码$")
                ).click()
                await page.wait_for_selector("div.publish-button")
            except Exception as e:
                logger.error(e)
                return
        await await_load_state(page)
        logger.info("登录创作服务平台成功")
        await save_cookies(cookie_file, page)

        logger.info(f"视频地址: {video_file_path}")
        await page.get_by_text("高清上传").hover()
        await page.get_by_text("发布视频", exact=True).click()
        page.once(
            "filechooser", lambda file_chooser: file_chooser.set_files(video_file_path)
        )
        await page.get_by_role("button", name="上传视频").click()
        await await_load_state(page)

        if json_file_path:
            title, description, tags = get_title_description_tags(json_file_path)

        if not title:
            title = os.path.splitext(os.path.basename(video_file_path))[0]
        if not description:
            description = ""
        if not tags:
            tags = ""

        # 填写标题和描述
        await page.locator("div").filter(has_text=re.compile(r"^0/500$")).locator(
            "div"
        ).fill(title + "\n" + description + "\n" + tags)
        logger.info("填写标题成功")

        # 发布
        logger.info("Publishing...")
        await page.pause()
        await page.get_by_role("button", name="发布").click()
        logger.info("发布成功")
