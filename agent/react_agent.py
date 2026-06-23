from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import  ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tootls import (rag_summarize,get_weather,get_user_id,
                                      get_user_location,get_current_month,fetch_external_data,fill_context_for_report)
from agent.tools.middleware import monitor_tool,log_befor_model,report_prompt_swithch
class ReactAgent:
    def __init__(self):
        self.agent=create_agent(
            model=ChatTongyi(model="qwen3-max"),
            system_prompt=load_system_prompts(),
            tools=[rag_summarize,get_weather,get_user_id,
                                      get_user_location,
                   get_current_month,fetch_external_data,fill_context_for_report],
            middleware=[monitor_tool,log_befor_model,report_prompt_swithch]
        )
    def execute_stream(self,query:str):
        input_dict={
            "messages":[
                {"role":"user","content":query},
            ]
        }
        for chunk in self.agent.stream(input_dict,stream_mode='values',context={"report":False}):
            latest_message=chunk["messages"][-1]
            yield latest_message.content.strip()+"\n"

if __name__ == '__main__':
    agent=ReactAgent()
    for text in agent.execute_stream("扫地机器人在我所在的地区如何保养,生成报告"):
        print(text, end="",flush=True)