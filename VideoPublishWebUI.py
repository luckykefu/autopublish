import argparse
import os
from src.demo_autopunlish import demo_auto_publish_video
from src.log import get_logger
import gradio as gr
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)


def parse_arguments():

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=f"{__file__}")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="Server name"
    )
    parser.add_argument("--server_port", type=int, default=None, help="Server port")
    parser.add_argument("--root_path", type=str, default=None, help="Root path")
    return parser.parse_args()


def main():
    args = parse_arguments()
    # Define the interface
    with gr.Blocks() as demo:
        with gr.TabItem("AutoPublishWebUI"):
            demo_auto_publish_video()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()
