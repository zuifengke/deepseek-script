import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# 加载 .env 文件中的环境变量
load_dotenv()

 # 从环境变量中获取 API 密钥
api_key = os.getenv("DEEPSEEK_API_KEY")

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

system_prompt = '''
  用户会提供一些文本信息，现在需要你将结果输出成name,region,height的json格式。
  样例输入：
  世界上最高的山是什么？

  期望输出的json格式：

  {
    "name": "珠穆朗玛峰",
    "region": "中国",
    "height": "8848米"
  }
'''

messages = [{'role':'system', 'content': system_prompt},{"role": "user", "content": "长沙最高的山是什么？"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
      'type':'json_object'
    }
)

messages.append(response.choices[0].message)

# print(response.choices[0].message.content)

print(json.loads(response.choices[0].message.content))