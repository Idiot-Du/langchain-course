from langchain_deepseek import ChatDeepSeek
from langchain.schema import AIMessage,HumanMessage,SystemMessage
import os

model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)
chat_history = []
system_message = SystemMessage(content="你是一个睿智的AI助手。")
chat_history.append(system_message)

while True:
    query = input("你：")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    print("助手：", response)

print("---对话历史---")
print(chat_history)