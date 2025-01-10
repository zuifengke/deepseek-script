from math import e
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key(model_name="deepseek-chat"):
    if(model_name == "deepseek-chat"):
        return os.getenv("DEEPSEEK_API_KEY")
    else:
        return os.getenv("GPT_API_KEY")

def send_messages(messages, use_tools = False):
    if(use_tools):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )
        return response.choices[0].message
    else:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
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
            "description": "Get weather of an location, the user should supply a location first",
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
message = send_messages(messages, use_tools=True)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "{'temperature':'25°C', 'humidity':'80%','weather':'cloudy'}"})
# 经过和openai的验证，这里一旦传入tools，deepseek-chat模型将重复输出tools的调用
message = send_messages(messages)
print(f"Model>\t {message.content}")
