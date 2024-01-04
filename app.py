import openai
import streamlit as st
from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from helper import check__menu
from langchain_core.runnables import RunnableBranch

st.title("ChatBot")

openai.api_key=st.secrets["api_secret"]
# pip install openai==0.27.8

# set the page icon
st.markdown('<link rel="shortcut icon" type="image/x-icon" href="chat_images.ico">', unsafe_allow_html=True)


menu=st.sidebar("Choose your type",("breakfast","coffee","main_course","starters","drinks"))

if menu:
    runnable_1 = RunnableLambda(check__menu)
    parser=StrOutputParser()

    menu_chain= (
    PromptTemplate.from_template(
            """List all the available {menu} . return name and their prices available in the menu"""
        )
        | runnable_1|parser
    )
    response=menu_chain.run(menu)

    st.write(response)

