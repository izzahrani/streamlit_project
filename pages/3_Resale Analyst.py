import pandas as pd
import numpy as np
import streamlit as st

  
try:
    _ = st.session_state.keep_graphics
except AttributeError:
    st.session_state.keep_graphics = False

DATE_COLUMN = 'quarter'
DATA = "./data/MedianResalePricesforRegisteredApplicationsbyTownandFlatType.csv"

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data = data[(data['price']!='na') & (data['price']!='-')]
    data['price'] = data['price'].astype('int')
    data['year'] = data[DATE_COLUMN].dt.year
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Report Analysis on Median Resale Price for a Town, HDB Type and Year')

from crewai import Agent, Task, Crew
from langchain.agents import Tool
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

df = pd.read_csv(DATA)
df = df[(df['price']!='na') & (df['price']!='-')]
df[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
df['price'] = df['price'].astype('float')
df['year'] = df[DATE_COLUMN].dt.year

pandas_tool_agent = create_pandas_dataframe_agent(
    llm=ChatOpenAI(temperature=0, model='gpt-4o-mini'),
    df=df, 
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True # <-- This is an "acknowledgement" that this can run potentially dangerous code
)

# Create the tool
pandas_tool = Tool(
    name="Manipulate and Analyze tabular data with Code",
    func=pandas_tool_agent.invoke,
    description="Useful for search-based queries",
)


# Creating Agents
agent_data_analyst = Agent(
    role="Content Planner",
    goal="Analyze the data based on user query: {topic}",
    backstory="""You're the best data analyst.""",
    allow_delegation=False,
	verbose=True,
    tools=[pandas_tool],
)

task_analyze = Task(
    description="""\
    1. Understand the user query: {topic}.
    2. Use the tool to analyze the data based on the user query.
    3. Develop a succinct report based on the analysis.""",

    expected_output="""\
    A succinct analysis report that present the results using McKinsey's Pyramid Principle.""",

    agent=agent_data_analyst,
)

# Creating the Crew
crew = Crew(
    agents=[agent_data_analyst],
    tasks=[task_analyze],
    verbose=True
)

with st.form("Input Parameters"):
    town = st.selectbox(
        "Which town would you like to analyse?",
        ("Ang Mo Kio", "Bedok", "Bishan", "Bukit Batok", "Bukit Merah", "Bukit Panjang", "Bukit Timah", "Central", "Choa Chu Kang", "Clementi", "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang/Whampoa", "Marine Parade", "Pasir Ris", "Punggol", "Queenstown", "Sembawang", "Sengkang", "Serangoon", "Tampines", "Toa Payoh", "Woodlands", "Yishun", "CENTRAL AREA"),
    )
    st.write("You selected:", town)

    flat_type = st.selectbox(
        "Which flat type would you like to analyse?",
        ("1-room", "2-room", "3-room", "4-room", "5-room", "Executive")
    )
    st.write("You selected:", flat_type)

    year = st.selectbox(
        "Which year would you like to analyse?",
        ("2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024")
    )
    st.write("You selected:", year)

    submitted = st.form_submit_button("Submit")


# Running the Crew
if submitted or st.session_state.keep_graphics: 
    result = crew.kickoff(inputs={"topic": f"What is the average median resale price for {town}, {flat_type} flat in {year}?"})
    st.markdown(result)
    st.session_state.keep_graphics = True

