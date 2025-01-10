from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_api_key():
    return os.getenv("GPT_API_KEY")

# model_info={
#     'url': 'https://api.gptapi.us/v1',
#     'api_key': get_api_key(),
#     'model': 'gpt-4o',
# }
model_info={
    'url': 'https://api.deepseek.com',
    'api_key': os.getenv("DEEPSEEK_API_KEY"),
    'model':'deepseek-chat'
}

client = OpenAI(
    api_key=model_info['api_key'],
    base_url=model_info['url'],
)

tools = [
  {
      "type": "function",
      "function": {
          "name": "get_weather",
          "parameters": {
              "type": "object",
              "properties": {
                  "location": {"type": "string"}
              },
          },
      },
  }
]

messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]
response = client.chat.completions.create(
  model=model_info['model'],
  messages=messages,
  tools=tools,
)

# simulate function call result message
function_call_result_message = {
  "role": "tool",
  "content": json.dumps({
      "weather": 'Sunny',
      "location": "Paris"
  }),
  "tool_call_id": response.choices[0].message.tool_calls[0].id
}

messages.append(response.choices[0].message)
messages.append(function_call_result_message)

print('-'*40)
print(f'The current model is {model_info["model"]}')
print('-'*40)

# 如果使用deepseek-chat模型，在发起新的对话时传入了tools参数，会导致生成的回复中再一次出现函数调用的结果。
# 但是，使用gtp-4o模型时，传入tools参数不会导致生成的回复中再次出现函数调用的结果。
# 因此，deepseek并未完全兼容openai的api接口。
response = client.chat.completions.create(
  model=model_info['model'],
  messages=messages,
  tools=tools,
)

print(response.choices[0].message)
