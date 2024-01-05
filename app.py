import openai
import json
import streamlit as st
from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from helper import check__menu
from langchain_core.runnables import RunnableBranch
from langchain.chains import SimpleSequentialChain

st.title("Welcome to the Restaurent Menu")


openai.api_key=st.secrets["api_secret"]
# pip install openai==0.27.8

menu=st.sidebar.selectbox("Choose your Menu type",("breakfast","coffee","main_course","starters","drinks"))

runnable_1 = RunnableLambda(check__menu)
parser=StrOutputParser()
template_m=PromptTemplate(input_variables=["menu"],output_variables="menu_item", template = "List all the available {menu} . return name and their prices available in the menu")
menu_chain= template_m| runnable_1|parser


ingrediants_chain=(PromptTemplate.from_template(
        """return ingredients of {item} to user. respond with a paragraph containing the ingredients"""
    )
    | runnable_1|parser
)


if menu:
    st.header(("Available " + menu+ " :"))
    response=menu_chain.invoke({"menu":menu})
    if menu in ["coffee","starters","drinks"]:
        response=response.split(',')
        for item in response:
            st.write("-",item)
            with st.expander("See ingredients"):
                 response_ing= ingrediants_chain.invoke({"item":item.split('-')[0].strip()}) 
                 st.write(response_ing)      

    else:
        response = response.replace("'", "\"")
        response=json.loads(response)
        for i, item in enumerate(response):
            formatted_response = f"{item['name']} - price: {item['price']}"
            st.write("-", formatted_response)
            with st.expander("See ingredients"):
                 response_ing= ingrediants_chain.invoke({"item":formatted_response.split('-')[0].strip()}) 
                 st.write(response_ing)


        
        
