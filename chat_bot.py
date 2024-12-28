import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

def create_chatbot():
    try:
        # 从环境变量中获取 API 密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        # print(f"API 密钥: {api_key}")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY 未设置，请在 .env 文件中配置。")

        # 初始化 OpenAI 客户端
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        # 初始化聊天记录
        messages = [
        ]

        print("聊天机器人已启动！输入 'exit' 或 'quit' 退出。")

        while True:
            # 获取用户输入
            user_input = input("\n你: ")
            if user_input.lower() in ["exit", "quit"]:
                print("聊天机器人: 再见！")
                break

            # 将用户输入添加到聊天记录
            messages.append({"role": "user", "content": user_input})

            # 创建流式请求
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True,
            )

            # 初始化机器人回复
            bot_response = ""
            print("聊天机器人: ", end="")

            # 逐步获取流式输出
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    bot_response += content

            # 将机器人回复添加到聊天记录
            messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    create_chatbot()