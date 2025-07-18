# coding: utf-8
'''
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-40")
result = model.invoke("what is 81 divided by 9?")

print("Full result:")
print(result)
print("Content only:")
print(result.content)
'''

from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

load_dotenv()

client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))
response = client.chat.completions.create(
    model = "glm-4",
    messages=[
        {"role": "user", "content": "布洛芬的用处?"}
    ],
)
print(response.choices[0].message)