from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

import gradio as gr

from dotenv import load_dotenv
import json
import requests
import os

load_dotenv('../../05_src/.secrets')
load_dotenv('../../05_src/.env')

from assignment_chat.prompts import return_instructions
from assignment_chat.tools_search import semantic_search
from assignment_chat.tools_jokes import get_jokes
from assignment_chat.tools_mcp_math import mcp_math

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

#Gradio User interface
# Attributed to https://www.gradio.app/guides/chatinterface-examples#lang-chain

import gradio as gr
from langchain.messages import AIMessage, HumanMessage  
from langchain_openai import ChatOpenAI  

model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0,
    base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
    api_key='any value',
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)
instructions = return_instructions()
tools = [semantic_search,get_jokes,mcp_math]

def predict(message, history):
    history_langchain_format = []
    for msg in history:
        if msg["role"] == "user":
            history_langchain_format.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            history_langchain_format.append(AIMessage(content=msg["content"]))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = model.invoke(history_langchain_format)
    return gpt_response.content


chatInterface = gr.ChatInterface(
    predict,
    api_name="chat",
)

#Will open at a localhost instance e.g., http://127.0.0.1:7860
chatInterface.launch()
