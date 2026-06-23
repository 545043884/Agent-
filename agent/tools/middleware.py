from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from langgraph.runtime import Runtime
from langgraph.types import  Command
from langchain_core.messages import  ToolMessage
from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompts,load_system_prompts

@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,#请求的数据封装
        handler:Callable[[ToolCallRequest],ToolMessage|Command] #执行的函数本身
)->ToolMessage | Command:
    logger.info(f"[Tool Monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[Tool Monitor]传入参数：{request.tool_call['args']}")
    try:
     res=handler(request)
     logger.info(f"[Tool Monitor]工具{request.tool_call['name']}调用成功")
     if request.tool_call["name"]=="fill_context_for_report":
         request.runtime.context["report"]=True
     return res
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，{str(e)}")
        raise e

@before_model
def log_befor_model(
        state: AgentState,  #整个agent智能体中的状态记录
        runtime: Runtime #记录了真个执行过程中的上下文我信息
):
    logger.info(f"[log_befor_model]即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_befor_model] {type(state['messages'][-1]).__name__} {state["messages"][-1].content.strip()}")
    return  None
@dynamic_prompt  #每次在生成提示词之前回调用此函数
def report_prompt_swithch(request: ModelRequest):
    is_report=request.runtime.context.get("report",False)
    if is_report:
       return load_report_prompts()
    return load_system_prompts()
