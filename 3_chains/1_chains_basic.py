from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser
import os

model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  
)

prompt_template = ChatPromptTemplate.from_messages([
    {"role":"system","content":"你是一个擅长讲关于{topic}笑话的大师。"},
    {"role":"user","content":"请给我讲{num}个关于{topic}的笑话。"}
])
#prompt = prompt_template.invoke({"topic":"小猫","num":"三"})

chain = prompt_template | model | StrOutputParser()
result = chain.invoke({"topic":"小猫","num":"三"})

print(result)

