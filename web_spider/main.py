import os
from turtle import st
from openai import OpenAI
from dotenv import load_dotenv
import httpx
import json

load_dotenv()

def spider(url):
    # 模拟浏览器的请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = httpx.get(url,headers=headers,follow_redirects=True)
   
    if response.status_code == 200:
        content = response.content.decode("gbk")
        return content
    else:
        return None

def create_parser(content:str):
    api_key = os.getenv('DEEPSEEK_API_KEY')
    client = OpenAI(api_key=api_key,base_url='https://api.deepseek.com')
    system_prompt = '''
    你是一位擅长分析网页的专家，请结构化输出这个网页的内容，将其表格中每一行的内容转换为结构化数据，输出的json格式为：
    {
        "code": "GB/T 12729.11-2008",
        "name":'香辛料和调味品 冷水可溶性抽提物的测定',
        "publish_date":'2008-11-01',
        "state":'现行'   
    }。
    最后将整个表格的内容输出为如上json格式的列表，
    输出的json为：{
        "standards":[
            {
               "code": "GB/T 12729.11-2008",
        "name":'香辛料和调味品 冷水可溶性抽提物的测定',
        "publish_date":'2008-11-01',
        "state":'现行'   
        }]}。
    '''
    messages = [{'role':'system', 'content': system_prompt},{"role": "user", "content": content}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type':'json_object'
        }
    )
    # messages.append(response.choices[0].message)
    return response.choices[0].message.content
    
def parse_content():
    pass
    
if __name__ == '__main__':
    url = 'http://www.csres.com/sort/industry/002006_2.html'
    content = spider(url)
    print('获取网页内容成功')
    if content:
        parser_content = create_parser(content)
        standards = json.loads(parser_content)['standards']
        print(f'检索标准{len(standards)}条')
        print(standards)
    else:
        print('Failed to get content')