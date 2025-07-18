from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langchain_community.chat_models import ChatZhipuAI, ChatBaichuan, ChatSparkLLM, ChatTongyi
import os

load_dotenv()

# 1. DeepSeek调用
messages = [HumanMessage(content="你是谁？")]
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  # 必须添加
)
response = model.invoke(messages)
print("DeepSeek:", response.content)
print("------------------")

# 2. 智谱AI调用
messages = [HumanMessage(content="你是谁？")]  # 用户消息
model = ChatZhipuAI(
    model="glm-4",
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY")
)
response = model.invoke(messages)
print("ZhipuAI:", response.content)
print("------------------")

# 3. 通义千问调用
messages = [HumanMessage(content="你是谁？")]
model = ChatTongyi(
    model="qwen-plus",
    dashscope_api_key=os.getenv("TONGYI_API_KEY")  # 需要添加
)
response = model.invoke(messages)
print("Tongyi:", response.content)
print("------------------")

