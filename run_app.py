import pandas as pd
from openai import OpenAI
import agents
import agents.field_selector_agent
from agents import dummy_agent
from utils.secrets import load_secrets
import os
import json
import argparse


def main(user_question):
    """
    Main function that runs the application.
    Args:
        user_question (str): The question to analyze
    """
    api_key = load_secrets()
    client = OpenAI(api_key=api_key)

    response = dummy_agent.run_agent(client, user_question)
    # Print the results in a more readable format
    print(response)
    


if __name__ == "__main__":
    # Example usage:
    # python run_app.py --question "What is machine learning and how does it relate to artificial intelligence?"
    parser = argparse.ArgumentParser(description='Analyze concepts using AI')
    parser.add_argument('--question', type=str, help='The question to analyze')
    
    args = parser.parse_args()
    main(args.question)
