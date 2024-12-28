import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_api_key():
    return os.getenv("DEEPSEEK_API_KEY")

def create_openai_client():
    client = OpenAI(api_key=get_api_key(),base_url="https://api.deepseek.com")
    return client

def create_chat(messages):
    client = create_openai_client()
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=messages,
    )
    return response.choices[0].message.content

if __name__ =='__main__':
    messages = [{'role':'user','content':'who are you?'}]
    response = create_chat(messages)
    print(response)