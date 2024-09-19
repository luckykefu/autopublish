import gradio as gr
from .clear_gradio_cache import clear_gradio_cache
from .auto_publish import save_title_description_tags
from .auto_publish_video_func.bjh import publish_to_bjh
from .auto_publish_video_func.xhs import publish_to_xhs
from .auto_publish_video_func.zhihu import publish_to_zhihu
from .auto_publish_video_func.blbl import publish_to_blbl
from .auto_publish_video_func.weibo import publish_to_weibo
from .auto_publish_video_func.dy import publish_to_dy
from .auto_publish_video_func.ks import publish_to_ks
from .auto_publish_video_func.sph import publish_to_sph
from .auto_publish_video_func.vivo import publish_to_vivo


def demo_auto_publish_video():
    gr.Markdown("## AutoPublishWebUI")
    gr.Markdown("### Clear Gradio Temp")
    clear_gradio_cache_btn = gr.Button("RUN", key="clear_cache")
    clear_gradio_cache_btn.click(fn=clear_gradio_cache)

    gr.Markdown("### Publishing Parameters")
    with gr.Row():

        video_file_path = gr.Video(label="Upload Video")

        with gr.Column():
            json_file_path = gr.File(
                label="Title, Description, Tags JSON File", type="filepath"
            )

            title = gr.Textbox(label="Title", value="", lines=1)
            description = gr.Textbox(label="Description", value="", lines=2)
            tags = gr.Textbox(label="Tags", value="#", lines=1)

        with gr.Column():
            json_output_path = gr.File(
                label="Save Title, Description, Tags as JSON File", type="filepath"
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
        xhs_btn = gr.Button("Publish to XHS")
        zhihu_btn = gr.Button("Publish to Zhihu")
        bili_btn = gr.Button("Publish to Bilibili")
        wb_btn = gr.Button("Publish to Weibo")
        dy_btn = gr.Button("Publish to Douyin")
        ks_btn = gr.Button("Publish to Kuaishou")
        sph_btn = gr.Button("Publish to Sph ")
        bjh_btn = gr.Button("Publish to Baijiahao")
        vivo_btn = gr.Button("Publish to Vivo ")

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
