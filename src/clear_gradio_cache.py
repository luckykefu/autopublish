import os
import shutil
import tempfile
from src.log import logger

f = os.path.basename(__file__)
logger.info(f)

def clear_gradio_cache():

    # 获取系统临时目录
    temp_dir = tempfile.gettempdir()

    # 构建 Gradio 缓存目录的路径
    gradio_cache_dir = os.path.join(temp_dir, 'gradio')

    # 检查目录是否存在
    if os.path.exists(gradio_cache_dir) and os.path.isdir(gradio_cache_dir):
        # 删除整个目录树
        shutil.rmtree(gradio_cache_dir)
        logger.info(f"Gradio cache directory '{gradio_cache_dir}' has been deleted.")
    else:
        logger.error(f"No Gradio cache directory found at '{gradio_cache_dir}'.")

if __name__ == '__main__':
    clear_gradio_cache()

