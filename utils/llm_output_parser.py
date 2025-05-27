import json

# parse the output of the LLM into JSON format
def parse_llm_json_output(raw_response: str) -> dict:
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        
        # Check if the response is wrapped in ```json and ``` tags
        json_start = raw_response.find("```json")
        json_end = raw_response.rfind("```")
        
        if json_start != -1 and json_end != -1:
            # Extract the JSON content
            json_content = raw_response[json_start + 7:json_end].strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError as e:
                print(f"Error parsing extracted JSON: {e}")

    
        # Check if the response is wrapped in ``` and ``` tags
        json_start = raw_response.find("```")
        json_end = raw_response.rfind("```")

        if json_start != -1 and json_end != -1:
            # Extract the Python code
            python_content = raw_response[json_start + 3:json_end].strip()
            return python_content

        
        # If extraction failed or wasn't possible, raise the original error
        print(f"Error parsing JSON response: {e}")
        raise ValueError("Invalid JSON response")
    

def parse_llm_python_output(raw_response: str) -> dict:

    # check if the response is wrapped in ```python and ``` tags
    python_start = raw_response.find("```python")
    python_end = raw_response.rfind("```")

    if python_start != -1 and python_end != -1:
        # Extract the Python code
        python_content = raw_response[python_start + 9:python_end].strip()
        return python_content
    
