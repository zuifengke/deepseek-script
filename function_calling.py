import json
import os
from json.decoder import JSONObject
from pyexpat import model
from turtle import mode
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据城市名称获取天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：上海、北京、深圳等",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

def get_weather(location):
    return f"{location} 的天气预报如下：晴天，气温 32摄氏度."

def get_api_key(model_name="deepseek-chat"):
    if(model_name == "deepseek-chat"  or model_name == "deepseek-reasoner"):
        return os.getenv("DEEPSEEK_API_KEY")
    else:
        return os.getenv("GPT_API_KEY")

model_name = "deepseek-chat"

def create_openai_client():
    client = OpenAI(api_key=get_api_key(),base_url="https://api.deepseek.com")
    # client = OpenAI(api_key=get_api_key(model_name),base_url="https://api.gptapi.us/v1")
    return client



def send_message(messages, use_tools = False):
    if(use_tools):
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )
    else :
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
    return response.choices[0].message



if __name__ =='__main__':
    client = create_openai_client()
    messages = [{'role':'user','content':'今天杭州的天气如何?'}]
    message = send_message(messages,True)
    tool = message.tool_calls[0]
    messages.append(message)
    if(len(message.tool_calls)>0):
        location = json.loads(message.tool_calls[0].function.arguments).get("location")
        function_name = message.tool_calls[0].function.name
        if(function_name == "get_weather"):
            # weather_info = get_weather(location)
            weather_info="{'温度':'25°C', '湿度':'80%','天气':'多云'}"
            # 将 weather_info 转换为 JSON 字符串
           # weather_info_str = json.dumps(weather_info, ensure_ascii=False)
            messages.append({"role": "tool", "tool_call_id": tool.id, "content": weather_info})
            message = send_message(messages)
            messages.append(message)
            print(message.content)
    print(messages)
