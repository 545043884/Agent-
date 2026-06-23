#总结服务类，用户提问问，搜索参考资料，将提问和参考提交给模型，
from langchain_core.documents import Document
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate

def print_prompt(prompt):
    print("+"*20)
    print(prompt.to_string())
    print("+"*20)
    return prompt
class RagSummarizeService(object):
    def __init__(self):
        self.vector_stor=VectorStoreService()
        self.retriever=self.vector_stor.get_retriever()
        self.model=ChatTongyi(model="qwen3-max", extra_body={"enable_thinking": False})
        self.prompt_text=load_rag_prompts()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.chain= self.__init__chain()
    def __init__chain(self):
        chain= self.prompt_template|print_prompt|self.model| StrOutputParser()
        return chain

    def retriever_docs(self, query : str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self,query : str)->str:
        context_docs=self.retriever_docs(query)
        context=""
        content=0
        for context_doc in context_docs:
            content +=1
            context += f"[参考资料{content}]：{context_doc.page_content}\n元数据：{context_doc.metadata}\n"
        return self.chain.invoke(
            {
                "input":query,
                "context":context,
            }
        )
if __name__ == '__main__':
    rag =RagSummarizeService()
    print(rag.rag_summarize("小户型适合那种机器人"))