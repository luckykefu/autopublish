import os

def get_script_filename():
    """
    获取当前脚本的完整路径
    :return: str
    """
    f = os.path.basename(__file__)
    s = os.path.splitext(f)[0]
    return s

if __name__ == '__main__':
    print(get_script_filename())