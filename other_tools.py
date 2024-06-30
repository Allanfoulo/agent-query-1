import pandas as pd
import re
from llama_index.core.tools import FunctionTool, ToolMetadata


def exact_match(input: str, survey_data: pd.DataFrame, column: str) -> list:
    """Searches for an exact match in the specified column of the survey data"""
    return survey_data[survey_data[column] == input][column].tolist()

def regex_search(input: str, survey_data: pd.DataFrame, column: str) -> list:
    """Searches for a pattern in the specified column of the survey data using regex"""
    pattern = re.compile(input)
    return survey_data[survey_data[column].str.contains(pattern)][column].tolist()

def column_search(input: str, survey_data: pd.DataFrame, columns: list) -> list:
    """Searches for keywords in the specified columns of the survey data"""
    results = []
    for column in columns:
        results.extend(survey_data[survey_data[column].str.contains(input)][column].tolist())
    return results



exact_match_tool = FunctionTool(
    exact_match, 
    ToolMetadata(
        name="exact_match", 
        description="Searches for an exact match in the survey data"
    )
)

regex_search_tool = FunctionTool(
    regex_search, 
    ToolMetadata(
        name="regex_search", 
        description="Searches for a pattern in the survey data using regex"
    )
)

column_search_tool = FunctionTool(
    column_search, 
    ToolMetadata(
        name="column_search", 
        description="Searches for keywords in specific columns of the survey data"
    )
)