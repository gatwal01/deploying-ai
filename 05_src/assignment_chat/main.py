from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

from dotenv import load_dotenv
import json
import requests
import os

from assignment_chat.prompts import return_instructions
from assignment_chat.tools_search import semantic_search
from assignment_chat.tools_jokes import get_jokes
from assignment_chat.tools_mcp_math import mcp_math
from utils.logger import get_logger


_logs = get_logger(__name__)
load_dotenv('../../05_src/.secrets')
load_dotenv('../../05_src/.env')

#Gradio User interface
# Attributed to https://www.gradio.app/guides/chatinterface-examples#lang-chain +
# main.py from course_chat sample project

model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0,
    base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
    api_key='any value',
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)
instructions = return_instructions()
tools = [semantic_search,get_jokes,mcp_math]



# @traceable(run_type="llm")
def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = model.bind_tools(tools).invoke( [SystemMessage(content=instructions)] + state["messages"])
    return {
        "messages": [response]
    }

def get_graph():
    
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph

