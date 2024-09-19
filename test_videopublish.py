# AutoPublishWebUI\TestAutoPublishWebUI.py
# --coding:utf-8--
# Time:2024-09-17 22:32:08
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)

######################################################
# TODO: xhs video publish

from src.auto_publish_video_func.xhs import publish_to_xhs
if __name__ == "__main__":
    import asyncio

    asyncio.run(
        publish_to_xhs(
            video_file_path=rf"D:\Videos\041.mp4",
            title=None,
            description=None,
            tags=None,
            json_file_path=None,
        )
    )

############################################################
# TODO: zhihu video publish

# from src.auto_publish_video_func.zhihu import publish_to_zhihu
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_zhihu(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

#########################################################
# TODO: wb video publish

# from src.auto_publish_video_func.weibo import publish_to_weibo
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_weibo(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

##############
# TODO: vivo video publish

# from src.auto_publish_video_func.vivo import publish_to_vivo
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_vivo(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

################################################################
# TODO: sph video publish

# from src.auto_publish_video_func.sph import publish_to_sph
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_sph(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

################################################
# TODO: ks video publish

# from src.auto_publish_video_func.ks import publish_to_ks
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_ks(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

##################################################################
# TODO: dy video publish

# from src.auto_publish_video_func.dy import publish_to_dy
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_dy(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )

#################################################################
# TODO: blbl video publish

# from src.auto_publish_video_func.blbl import publish_to_blbl
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_blbl(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     ) 
    

###########################################################################
# TODO: bjh video publish

# from src.auto_publish_video_func.bjh import publish_to_bjh
# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(
#         publish_to_bjh(
#             video_file_path=rf"D:\Videos\041.mp4",
#             title=None,
#             description=None,
#             tags=None,
#             json_file_path=None,
#         )
#     )   

