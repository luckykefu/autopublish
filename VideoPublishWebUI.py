import argparse
import os
from src.log import get_logger
import gradio as gr

from src.auto_publish_video_func.blbl import publish_to_blbl
from src.auto_publish_video_func.xhs import publish_to_xhs
from src.auto_publish_video_func.zhihu import publish_to_zhihu
from src.auto_publish_video_func.weibo import publish_to_weibo
from src.auto_publish_video_func.dy import publish_to_dy
from src.auto_publish_video_func.ks import publish_to_ks
from src.auto_publish_video_func.sph import publish_to_sph
from src.auto_publish_video_func.bjh import publish_to_bjh
from src.auto_publish_video_func.vivo import publish_to_vivo
from src.auto_publish import save_title_description_tags
from src.clear_gradio_cache import clear_gradio_cache
from dotenv import load_dotenv
load_dotenv()
logger = get_logger(__name__)

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)


def main():
    # Define the interface
    with gr.Blocks() as demo:
        with gr.TabItem("AutoPublishWebUI"):
            gr.Markdown("## AutoPublishWebUI")
            gr.Markdown("### 清除gradio缓存")
            clear_cache_btn = gr.Button("RUN", key="clear_cache")
            clear_cache_btn.click(fn=clear_gradio_cache)

            gr.Markdown("### 发布参数")
            with gr.Row():

                video_file_path = gr.Video(label="上传视频")

                with gr.Column():
                    json_file_path = gr.File(
                        label="标题描述标签json文件", type="filepath"
                    )

                    title = gr.Textbox(label="标题", value="", lines=1)
                    description = gr.Textbox(label="描述", value="", lines=2)
                    tags = gr.Textbox(label="标签", value="#", lines=1)

                with gr.Column():
                    json_output_path = gr.File(
                        label="保存标题描述标签为json文件", type="filepath"
                    )

            title.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )
            description.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )
            tags.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )

            with gr.Row():
                xhs_btn = gr.Button("发布到xhs")
                zhihu_btn = gr.Button("发布到知乎")
                bili_btn = gr.Button("发布到哔哩哔哩")
                wb_btn = gr.Button("发布到微博")
                dy_btn = gr.Button("发布到抖音")
                ks_btn = gr.Button("发布到快手")
                sph_btn = gr.Button("发布到视频号")
                bjh_btn = gr.Button("发布到百家号")
                vivo_btn = gr.Button("发布到Vivo号")

            xhs_btn.click(
                fn=publish_to_xhs,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            bili_btn.click(
                fn=publish_to_blbl,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            dy_btn.click(
                fn=publish_to_dy,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            ks_btn.click(
                fn=publish_to_ks,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            wb_btn.click(
                fn=publish_to_weibo,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            sph_btn.click(
                fn=publish_to_sph,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            bjh_btn.click(
                fn=publish_to_bjh,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            vivo_btn.click(
                fn=publish_to_vivo,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            zhihu_btn.click(
                fn=publish_to_zhihu,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )

    # Launch the interface
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="server name"
    )
    parser.add_argument("--server_port", type=int, default=8080, help="server port")
    parser.add_argument("--root_path", type=str, default=None, help="root path")
    args = parser.parse_args()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()
