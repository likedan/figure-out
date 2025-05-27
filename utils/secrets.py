import json
def load_secrets() -> str:
    """Load API key from secrets.json file"""
    try:
        with open('data/secrets.json', 'r') as f:
            secrets = json.load(f)
            return secrets['openai_api_key']
    except FileNotFoundError:
        raise Exception("secrets.json file not found. Please create it with your OpenAI API key.")
    except KeyError:
        raise Exception("openai_api_key not found in secrets.json")
