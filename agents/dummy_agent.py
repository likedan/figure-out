'''
This is a dummy agent that processes data based on the user request by creating knowledge graphs. It serves as a placeholder for testing and demonstration purposes.
'''


from openai import OpenAI

def run_agent(client: OpenAI, user_message: str) -> str:

    input_user_prompt = user_message

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_user_prompt}
        ]
    )

    raw_response = completion.choices[0].message.content
 
    return raw_response
