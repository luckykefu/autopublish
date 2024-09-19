# What is AutoPublish?

just a auto publish tool in video and article

# Features

## Video Publish

- [x] Publish video to xhs
- [x] Publish video to bilibili
- [x] Publish video to baijiahao
- [x] Publish video to douyin
- [x] Publish video to kuaishou
- [x] Publish video to sph
- [x] Publish video to weibo
- [x] Publish video to zhihu
- [x] Publish video to vivo

## Article Publish

# Usage

To use AutoPublish, you need to follow these steps:

1. Install Python 3.x and pip.
2. Install AutoPublish by running the following command in your terminal:

```
git clone https://github.com/xhs/AutoPublish.git
cd AutoPublish
pip install -r requirements.txt
playwright install chromium

# change the .env_example file to .env and fill in the necessary information
cp .env_example .env

python webui.py

```
