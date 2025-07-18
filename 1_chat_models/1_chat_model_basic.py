# -*- coding: utf-8 -*-
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


#from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import os

api_key = os.getenv("ZHIPUAI_API_KEY")
chat = ChatZhipuAI(
    model = "glm-4",
    temperature = 0.5,
)
message = [
    {"role": "user", "content": "布洛芬可以治疗痛经吗?"},
]
response = chat.invoke(message)
print(response.content)


'''
from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

load_dotenv()

client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))
response = client.chat.completions.create(
    model = "glm-4",
    messages=[
        {"role": "user", "content": "布洛芬可以治疗痛经吗?"}
    ],
)
print(response.choices[0].message)
'''

