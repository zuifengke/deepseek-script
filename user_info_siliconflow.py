import requests

url = "https://api.siliconflow.cn/v1/user/info"

headers = {"Authorization": "Bearer sk-nmhcrymaktgoupxtlfufbomowoohjsnfzrhkpbcejdjutgos"}

response = requests.request("GET", url, headers=headers)

print(response.text)