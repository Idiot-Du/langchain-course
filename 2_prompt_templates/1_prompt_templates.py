from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# template = "给我讲个关于{topic}的笑话"
# prompt_template = ChatPromptTemplate.from_template(template)
# print("-------模板-------")
# prompt = prompt_template.invoke({"topic":"小猫"})
# print(prompt)

# template_multiple = """你是一个智能助手，你的任务是回答用户的问题。
# Human:给我讲一个{adjective}的笑话，主题关于{animal}的。
# Assistant:
# """
# prompt_template_multiple = ChatPromptTemplate.from_template(template_multiple)
# prompt = prompt_template_multiple.invoke({"adjective":"血腥的","animal":"犀牛"})
# print(prompt)
# print(prompt.to_string())

# messages = [
#     {"role":"system","content":"你是一个讲笑话的大师，擅长讲关于{topic}的笑话。"},
#     {"role":"human","content":"给我讲{joken_count}个笑话。"},
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic":"小猫","joken_count":3})
# print(prompt)
# print(prompt.to_string())

messages = [
    {"role":"system","content":"你是一个{topic}领域的专家，负责解决用户的问题。"},
    {"role":"human","content":"你好，我想知道关于{question}的答案。"},
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic":"小猫","question":"猫咪表达友好的方式"})
print(prompt)
print(prompt.to_string())