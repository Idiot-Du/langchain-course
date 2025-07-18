from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
import os
model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  
)
print("-----prompt from template-----")
messages = [
    {"role":"user","content":"给我讲一个关于{topic}的笑话"}
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic":"小猫"})
result = model.invoke(prompt)
print(result.content)