'''
This agent is designed to generate code for a given task.
'''

SYSTEM_PROMPT = '''
You are a code generation assistant. Your task is to produce executable Python code based on the given requirements. Follow these guidelines:

1. Generate only Python code, using standard library modules exclusively.
2. Strictly adhere to the provided input and output format.
3. Ensure the code is efficient, well-structured, and follows Python best practices.
4. Include error handling and input validation where necessary.
5. Add concise comments for clarity on complex logic.
6. Verify the code meets all specified requirements.
7. Ensure compatibility with Python 3.x versions.
8. Return only one function named "process_data".
9. The process_data function should take a pandas DataFrame as input and return the specified output type.

Your response should contain only the generated code for the process_data function, without any additional explanations or markdown formatting. The function will be called directly in the code execution.
'''

from openai import OpenAI
import pandas as pd
from utils.llm_output_parser import parse_llm_python_output

def run_agent(client: OpenAI, user_message: str, output_type: str, input_data: pd.DataFrame) -> tuple[str, type]:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""Generate Python code for the following task:

Task description: {user_message}

function should take a parameter input_data of type pandas DataFrame and return a pandas DataFrame as output.

Output type: {output_type}

Input DataFrame:
{input_data.head().to_string()}

Your code should take a pandas DataFrame as input and return output_type.
"""}
        ]
    )

    raw_response = completion.choices[0].message.content
    print(raw_response)
    code = parse_llm_python_output(raw_response)
    print(code)

    # check if the code is executable python code
    try:
        # only give top 10 rows of the input data
        input_data_sample = input_data.head(10)
        # Execute the code to define the process_data function
        exec(code, globals())
        # Call the process_data function with input_data_sample
        output = process_data(input_data_sample)
    except Exception as e:
        print(f"Error: {e}")
        return False, "Code is not executable"

   # as long as return is not None, we are good
    if output is None:
        return False, "Code is not returning anything"

    return code, type(output)