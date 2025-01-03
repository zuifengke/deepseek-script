import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

 # 从环境变量中获取 API 密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
# print(f"API 密钥: {api_key}")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY 未设置，请在 .env 文件中配置。")


# Define the calculator functions
def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

# Tools definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["a", "b"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["a", "b"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "divide two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["a", "b"]
            },
        }
    },
]

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)


messages = [{'role':'system','content':'You are a helpful assistant that solves math problems step by step.'},{"role": "user", "content": "Calculate (3*3+4)*12+22"}]
message = send_messages(messages)
messages.append(message)
print(f"User>\t {messages[0]['content']}")
print(f"Model>\t {message}")
tool = message.tool_calls[0]
function_name = tool.function.name
arguments = json.loads(tool.function.arguments)
print(f"Model>\t function_name:{function_name},arguments:{arguments}")

# if(function_name == 'multiply'):
#     a = arguments['a']
#     b = arguments['b']
#     result = multiply(a, b)
#     print(f"function>\t result:{result}")
#     messages.append({"role": "tool", "tool_call_id": tool.id, "content": json.dumps({"result": result})})
#     # print(messages)
#     message = send_messages(messages)
#     print(f"Model>\t {message.content}")

