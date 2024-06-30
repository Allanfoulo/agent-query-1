import streamlit as st
import os
import pandas as pd
from logic import create_query_engine, create_react_agent, process_query

st.title("Agent Query Application")
st.write("Query the survey data or upload your own custom CSV/Excel files!")

uploaded_file = st.file_uploader("Upload a CSV or Excel file:", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
else:
    survey_path = os.path.join("data", "survey.xlsx")
    df = pd.read_excel(survey_path)

query_engine = create_query_engine(df)
agent = create_react_agent(query_engine)

# Store the agent in the session state
if 'agent' not in st.session_state:
    st.session_state.agent = agent

query_input = st.text_input("Enter a query:", placeholder="What do you want to know?")
submit_button = st.button("Ask")


if submit_button:
    if 'agent' in st.session_state:
        initialized_agent = st.session_state.agent
        print("Query input:", query_input)  # Debug print statement
        result, thought_process = process_query(initialized_agent, query_input)
        if isinstance(result, str):
            st.write(result)  # Display the response text
        else:
            response_text = result.response  # Extract the response text
            st.write(response_text)  # Display the response text
        
        # Display the thought process text
        st.write(thought_process)
        
    else:
        st.write("Agent is not initialized.")
