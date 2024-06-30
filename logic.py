from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.llms.groq import Groq
from prompt import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent.react import ReActAgent
from other_tools import exact_match_tool, regex_search_tool,column_search_tool


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm_model = Groq(model="llama3-70b-8192", api_key=groq_api_key)

def create_query_engine(df):
    query_engine = PandasQueryEngine(df=df, verbose=True, instruction_str=instruction_str, llm=llm_model)
    query_engine.update_prompts({"pandas_prompt": new_prompt})
    return query_engine

def create_react_agent(query_engine):
    tools = [
        note_engine,
        QueryEngineTool(
            query_engine=query_engine, 
            metadata=ToolMetadata(
                name="survey_data",
                description="The spreadsheet contains data from a survey conducted with interns at Unified Mentor. The survey consists of multiple sections that cover different aspects of the interns' demographics, internship experience, and their feedback on the internship program."
            )
        ),
        exact_match_tool,
        regex_search_tool,
        column_search_tool
    ]

    # Pass survey_data as a parameter when calling the functions
    exact_match_tool_fn = lambda input, column: exact_match_tool(survey_data=query_engine.df, input=input, column=column)
    regex_search_tool_fn = lambda input, column: regex_search_tool(survey_data=query_engine.df, input=input, column=column)
    column_search_tool_fn = lambda input, columns: column_search_tool(survey_data=query_engine.df, input=input, columns=columns)

    # Use ReActAgent with a focus on direct return
    agent = ReActAgent.from_tools(tools, llm=llm_model, verbose=True, context=context, return_direct=True,  max_iterations=200)
    return agent


def process_query(agent, query):
    try:
        print("Processing query...")
        result = agent.query(query)
        print("Query result:", result)
        
        thought_process = st.empty()
        thought_process = "Thinking about the input... "
        thought_process += "Generating response... "
        
        return result, thought_process
    except Exception as e:
        print("Error:", e)
        return str(e), ""
