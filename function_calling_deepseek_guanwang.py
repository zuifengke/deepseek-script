from openai import OpenAI

#model_name='deepseek-reasoner'
model_name='deepseek-chat'
def send_messages(messages, use_tools = False):
    if use_tools:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )
        return response.choices[0].message
    else:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message

client = OpenAI(
    api_key="sk-c42402d9915948e29ac361d7aada066c",
    base_url="https://api.deepseek.com",
)

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

messages = [{"role": "user", "content": "杭州的天气如何?"}]
message = send_messages(messages,True)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "{'温度':'25°C', '湿度':'80%','天气':'多云'}"})
message = send_messages(messages)
print(f"Model>\t {message.content}")