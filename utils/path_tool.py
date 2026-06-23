import  os
def get_project_root() ->str:
    current_file=os.path.abspath(__file__) #获取工程根目录，先获取文件所在的绝对路径
    current_dir=os.path.dirname(current_file) #获取文件所在的文件加
    current_root=os.path.dirname(current_dir) #获取工程根目录
    return current_root


def get_abs_path(relative_path:str) ->str:
    project_root=get_project_root()
    return os.path.join(project_root,relative_path)

