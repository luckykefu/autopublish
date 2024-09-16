import json


async def save_cookies(cookie_file, page):
    print("save cookies")
    cookies = await page.context.cookies()
    with open(cookie_file, "w") as f:
        json.dump(cookies, f, indent=4)