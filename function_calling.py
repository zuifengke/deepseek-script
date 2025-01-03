import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_api_key():
    return os.getenv("DEEPSEEK_API_KEY")

def get_weather(location):
    if(location == 'Hangzhou'):
        return '{"temperature": 24, "description": "clear sky"}'

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key=get_api_key(),
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
message = send_messages(messages)
messages.append(message)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
function_name = tool.function.name
arguments = json.loads(tool.function.arguments)
print(f"Model>\t function_name:{function_name},arguments:{arguments}")
if(function_name == 'get_weather'):
    location = arguments['location']
    weather = get_weather(location)
    print(f"function>\t weather:{weather}")
    messages.append({"role": "tool", "tool_call_id": tool.id, "content": weather})
    # print(messages)
    message = send_messages(messages)
    print(f"Model>\t {message.content}")

