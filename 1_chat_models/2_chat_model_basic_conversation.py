from langchain_community.chat_models import ChatZhipuAI
import os
#from dotenv import load_dotenv

#load_dotenv()

chat = ChatZhipuAI(
    api_key = os.getenv("ZHIPUAI_API_KEY"),
    model = "glm-4",
    temperature = 0.5,
)
messages = [
    {"role":"system","content":"你是一个智能助手，会主动解决问题并回答用户的疑惑。"},
    {"role":"user","content":"81除以9等于多少？"},
    {"role":"assistant","content":"81除以9等于9。如果您有任何其他问题或需要帮助，请随时告诉我！"},
    {"role":"user","content":"128除以9等于多少？"},
]
response = chat.invoke(messages)
print(response.content)