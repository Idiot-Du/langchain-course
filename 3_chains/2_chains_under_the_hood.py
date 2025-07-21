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
format_template = RunnableLambda(lambda x:prompt_template.format_prompt(**x))
invoke_model = RunnableLambda(lambda x:model.invoke(x.to_messages()))
parse_output = RunnableLambda(lambda x:x.content)

chain = RunnableSequence(first=format_template,middle=[invoke_model],last=parse_output)
result = chain.invoke({"topic":"小猫","num":"三"})

print(result)

