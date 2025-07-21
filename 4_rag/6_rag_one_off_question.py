import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_community.embeddings import ZhipuAIEmbeddings

load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir,"db","chroma_db_with_metadata")

embedding = ZhipuAIEmbeddings(
    model = "embedding-3",
    api_key = os.getenv("ZHIPUAI_API_KEY"),
)
db = Chroma(persist_directory=persistent_dir,embedding_function=embedding)

query = "大语言模型是什么？"

retriever = db.as_retriever(
    search_type = "similarity_score_threshold",
    search_kwargs = {"k":1,"score_threshold":0.2}
)
relevant_docs = retriever.invoke(query)

combine_input = (
    "这是一些对于回答可能有用的文档" +
    "\n" +
    "\n".join([doc.page_content for doc in relevant_docs]) +
    "\n" +
    "请根据以上文档回答问题" +
    query
)
model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)
messages = [
    {"role":"user","content":combine_input},
]
result = model.invoke(messages)
print(result)
print("\n-----------\n")
print(result.content)