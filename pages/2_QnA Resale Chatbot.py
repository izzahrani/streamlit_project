from openai import OpenAI
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from helper_functions.llm import get_completion, get_embedding, get_completion_by_messages, count_tokens_from_message, count_tokens
import requests


st.title("QnA Resale Chatbot") 

file_path="./data/hdb_2.html"

# urls = ["https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/overview",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/planning-considerations",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/mode-of-financing",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/option-to-purchase",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/request-for-value",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/application",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/acceptance-and-approval",
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/request-for-enhanced-contra-facility"
#         "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-completion"]

### Step 1: Document Loading
from langchain_community.document_loaders import BSHTMLLoader
from bs4 import BeautifulSoup

loader = BSHTMLLoader(file_path ,bs_kwargs={'features': 'html.parser'})
data = loader.load()


### Step 2: Splitting & Chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter_ = RecursiveCharacterTextSplitter(
    separators=["\n\n\n","\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50,
    length_function=count_tokens
)

splitted_documents = text_splitter_.split_documents(data)

### Step 3: Storage - Embedding & Vectorize
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# An embeddings model is initialized using the OpenAIEmbeddings class.
# The specified model is 'text-embedding-3-small'.
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')

vector_store = Chroma.from_documents(
    collection_name="combined_docs",
    documents=splitted_documents,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
)

vector_store = Chroma("combined_docs",
                      embedding_function=embeddings_model,
                      persist_directory= "./chroma_langchain_db")

### Step 4: Retrieval
# vector_store.similarity_search_with_relevance_scores('Zero Shot', k=3)

### Step 5: Q&A

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Run chain

def generate_response(input_text):
    qa_chain = RetrievalQA.from_chain_type(
                ChatOpenAI(model='gpt-4o-mini'),
                retriever=vector_store.as_retriever(),
                return_source_documents=True, # Make inspection of document possible
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    st.info(qa_chain.invoke(input_text)['result'])


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the steps in making a HDB resale purchase?",
    )
    submitted = st.form_submit_button("Submit")
    generate_response(text)