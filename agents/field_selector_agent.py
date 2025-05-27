# agents/field_selector_agent.py

'''
This agent is designed to determine the fields in uploaded tables that should be used and the type of output that should be generated.
'''

import pandas as pd
from openai import OpenAI
import json
from utils.llm_output_parser import parse_llm_json_output


SYSTEM_PROMPT = '''
You are an AI agent designed to determine the fields in uploaded tables that should be used and the type of output that should be generated.

Your output should be strictly structured JSON that can be parsed. The JSON should include:
1. A list of fields to be used from the uploaded tables, including both the dataframe index and the field name.
2. The type of output that should be generated.

IMPORTANT: You must only select fields that are explicitly listed in the provided table information. Do not invent or hallucinate any field names. If a field you want to use is not present in the given data, do not include it.

Example output format:
{
    "selected_fields": [
        {"dataframe": 0, "field": "field1"},
        {"dataframe": 1, "field": "field2"},
        {"dataframe": 0, "field": "field3"}
    ],
    "output_type": "data_col(s)"
}

Note: The output_type should be one of the following:
- "data_col(s)": for generating a new column(s) of data
- "other": for any other type of output

Before finalizing your response, double-check that:
1. All fields in "selected_fields" exist in the tables provided.
2. The dataframe indices are valid (0 to n-1, where n is the number of tables).
3. The output_type is one of the allowed types.

If you're unsure about a field's existence, exclude it from your selection.
'''

ALLOWED_OUTPUT_TYPES = ["data_col(s)", "other"]

def run_agent(client: OpenAI, user_message: str, dfs: list[pd.DataFrame]) -> dict:

    user_message_part_of_prompt = f'''
User message: {user_message}

Available tables and their fields:
'''
    for i, df in enumerate(dfs):
        user_message_part_of_prompt += f'''
Table {i}:
  Shape: {df.shape}
  Fields:
{chr(10).join(f"    - {col}" for col in df.columns)}
  Sample data (first row):
{df.head(1).to_string(index=False)}
    '''
    
    # TODO: Implement logic to handle different table sizes and adjust the number of rows shown accordingly


    completion = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}] +
            [{"role": "assistant", "content": user_message_part_of_prompt},])

    raw_response = completion.choices[0].message.content
    print(raw_response)
    json_response = parse_llm_json_output(raw_response)

    # validate json_response
    if not isinstance(json_response, dict):
        raise ValueError("Invalid JSON response")
    if "selected_fields" not in json_response:
        raise ValueError("selected_fields not found in JSON response")
    if "output_type" not in json_response:
        raise ValueError("output_type not found in JSON response")
    # validate selected_fields
    if not isinstance(json_response["selected_fields"], list):
        raise ValueError("selected_fields is not a list")
    for field in json_response["selected_fields"]:
        if not isinstance(field, dict):
            raise ValueError("selected_fields contains non-dict items")
        if "dataframe" not in field:
            raise ValueError("dataframe not found in selected_fields")
        if "field" not in field:
            raise ValueError("field not found in selected_fields")
        # verify that the field exists in the dataframe
        df_index = field["dataframe"]
        column_name = field["field"]
        if df_index >= len(dfs) or column_name not in dfs[df_index].columns:
            raise ValueError(f"Field '{column_name}' not found in Table {df_index}")
    
    # validate output_type
    if json_response["output_type"] not in ALLOWED_OUTPUT_TYPES:
        raise ValueError(f"output_type is not one of the allowed types: {ALLOWED_OUTPUT_TYPES}")
    
    return json_response
