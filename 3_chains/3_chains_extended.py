from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser
import os
from langchain.schema.runnable import RunnableLambda,RunnableSequence

model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  
)

prompt_template = ChatPromptTemplate.from_messages([
    {"role":"system","content":"你是一个擅长讲关于{topic}笑话的大师。"},
    {"role":"user","content":"请给我讲{num}个关于{topic}的笑话。"}
])

uppercase_output = RunnableLambda(lambda x:x.upper())
count_words = RunnableLambda(lambda x:f"word count:{len(x.split())}\n{x}")

chain = prompt_template | model | StrOutputParser() | uppercase_output | count_words
result = chain.invoke({"topic":"小猫","num":"三"})

print(result)

