import pandas as pd
from openai import OpenAI
import agents
import agents.field_selector_agent
from agents import dummy_agent, process_data_by_row, generate_code_vs_llm, code_generator, process_data_by_row, process_data_by_row_batched
from utils.secrets import load_secrets

import argparse

def main(user_question):
    """
    Main function that runs the application.
    Args:
        user_question (str): The question to analyze
    """

    api_key = load_secrets()
    client = OpenAI(api_key=api_key)

    results = agents.figure_out_related_concepts.run_agent(client, user_question)
    # Print the results in a more readable format
    print("\nAnalysis Results:")
    print("================")
    print(f"\nMain Concept: {results['main_concept']}")
    print("\nRelated Concepts:")
    for concept in results['related_concepts']:
        print(f"\n• {concept['name']} ({concept['type']})")
        print(f"  Relation: {concept['relation']}")
        print(f"  Description: {concept['description']}")
        print(f"  Diagnostic Question: {concept['diagnostic_question']}")
    


if __name__ == "__main__":
    # Example usage:
    # python run_app.py --question "What is machine learning and how does it relate to artificial intelligence?"
    parser = argparse.ArgumentParser(description='Analyze concepts using AI')
    parser.add_argument('--question', type=str, help='The question to analyze')
    
    args = parser.parse_args()
    main(args.question)
