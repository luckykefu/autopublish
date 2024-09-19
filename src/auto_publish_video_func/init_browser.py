import os
from ..log import get_logger

logger = get_logger(__name__)
from dotenv import load_dotenv

load_dotenv()
chrome_path = os.getenv("CHROME_PATH")


async def init_browser(p):
    # Launch persistent browser context
    logger.info("Initializing browser...")
    browser = await p.chromium.launch_persistent_context(
        user_data_dir=None,  # User data directory
        executable_path=chrome_path,  # Specify browser path
        accept_downloads=True,  # Accept downloads
        headless=False,  # Headless mode
        bypass_csp=True,  # Bypass CSP
        slow_mo=20,  # Slow motion
        args=[
            "--disable-blink-features=AutomationControlled"
        ],  # Disable automation detection
    )
    logger.info("Browser initialized successfully.")
    # Set default timeout
    browser.set_default_timeout(600 * 1000)  # 10 minutes

    return browser
