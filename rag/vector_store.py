import os.path
from langchain_core.documents import Document

from langchain_chroma import  Chroma
from utils.path_tool import  get_abs_path
from utils.config_handler import chroma_conf
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader,text_loader,listdir_with_allowed_type,get_file_md5_hex
from utils.logger_handler import logger
class VectorStoreService:
    def __init__(self):
        self.vector_store=Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=DashScopeEmbeddings(model="text-embedding-v1"),
            persist_directory=get_abs_path(chroma_conf["persist_directory"])
        )
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":chroma_conf["k"]})
    def load_document(self):
        def check_md5(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip()==md5_for_check:
                        return True
                return  False
        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_check+"\n")
        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
                return text_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            return []
        allowed_files_path:list[str]=listdir_with_allowed_type(get_abs_path(chroma_conf["data_path"]),
                                                               tuple(chroma_conf.get("allow_knowwledge_file_type")))
        for file_path in allowed_files_path:
            md5_hex=get_file_md5_hex(file_path)
            if check_md5(md5_hex):
                logger.info(f"[加载知识库],{file_path}内容已存在")
                continue
            try:
                documents:list[Document]=get_file_documents(file_path)
                if not documents:
                    logger.warning("文件内没有内容")
                    continue
                split_document: list[Document]=self.spliter.split_documents(documents)
                if not split_document:
                    logger.warning("分片后没有文本内容，跳过")
                    continue
                self.vector_store.add_documents(split_document)
                save_md5_hex(md5_hex)
                logger.info(f"当前知识库加载完成{file_path}")
            except Exception as e:
                logger.error(f"[知识库加载失败]{file_path},{str(e)}",exc_info=True)
                continue

if __name__ == '__main__':
     vs=VectorStoreService()
     vs.load_document()
     retriver=vs.get_retriever()
     res=retriver.invoke("迷路")
     for r in res:
         print(r.page_content)