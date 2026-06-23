
import  os,hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader,PyPDFLoader


def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"md5文件{filepath}不存在")
        return
    if not os.path.isfile(filepath):
        logger.error(f"md5文件{filepath}不是文件")
        return
    md5_obj=hashlib.md5()
    chunk_szie=4096
    try:
        with open(filepath, 'rb') as f:
            while chunk :=f.read(chunk_szie):
                md5_obj.update(chunk)

        md5_hax=md5_obj.hexdigest()
        return md5_hax
    except Exception as e:
        logger.error(f"计算文件按{filepath}md5失败，{str(e)}")
        return None
def listdir_with_allowed_type(path:str ,allowwed_types:tuple[str]): #返回文件夹得文件列表，（允许得后缀）
    files=[]
    if not os.path.isdir(path):
        logger.error("不是文件夹，不进行处理")
        return allowwed_types
    for f in os.listdir(path):
        if f.endswith(allowwed_types):
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(filepath:str ,passworld=None) ->list[Document]:
    return PyPDFLoader(filepath,passworld).load()

def text_loader(filepath:str)->list[Document]:
    return TextLoader(filepath,encoding="utf-8").load()
