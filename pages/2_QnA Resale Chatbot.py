from openai import OpenAI
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

st.title("QnA Resale Chatbot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



# def generate_response(input_text):
#     model = ChatOpenAI(temperature=0.7, api_key=OPENAI_API_KEY)
#     st.info(model.invoke(input_text))


# with st.form("my_form"):
#     text = st.text_area(
#         "Enter text:",
#         "What are the three key pieces of advice for learning how to code?",
#     )
#     submitted = st.form_submit_button("Submit")
#     if not OPENAI_API_KEY.startswith("sk-"):
#         st.warning("Please enter your OpenAI API key!", icon="⚠")
#     if submitted and OPENAI_API_KEY.startswith("sk-"):
#         generate_response(text)