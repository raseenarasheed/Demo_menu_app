
import json
from pathlib import Path
import streamlit as st
from langchain_community.llms.openai import OpenAI
from langchain_community.tools.json.tool import JsonSpec
from langchain_community.agent_toolkits import JsonToolkit

openai_api_key=st.secrets["api_secret"]

def create_json_agent():
    # read json file
    with open("restaurant_menu.json",'r') as f:
        data = json.load(f)
    json_spec = JsonSpec(dict_=data, max_value_length=4000)
    json_toolkit = JsonToolkit(spec=json_spec)

    json_agent_executor = create_json_agent(
    llm=OpenAI(openai_api_key=openai_api_key,temperature=0), toolkit=json_toolkit, verbose=False)

    return json_agent_executor

def check__menu(type_prompt: str) -> str:
    json_agent_executor=create_json_agent()
    response=json_agent_executor.run(type_prompt)
    return response

