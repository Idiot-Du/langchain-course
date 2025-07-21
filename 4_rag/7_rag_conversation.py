from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import TextSplitter
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir,"db","chroma_db_with_metadata")

embeddings = ZhipuAIEmbeddings(
    model = "embedding-3",
    api_key = os.getenv("ZHIPUAI_API_KEY"),
)
chat = ChatDeepSeek(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)
query = "大语言模型的应用场景有哪些？"
db = Chroma(embedding_function=embeddings,persist_directory=persistent_dir)
retriever = db.as_retriever(
    search_type = "similarity_score_threshold",
    search_kwargs = {"k":1,"score_threshold":0.2}
)

contextualize_q_system_prompt = (
    "你是一个问答助手，你的任务是回答用户的问题。"
    "用户的问题是：{question}"
    "你需要根据用户的问题和相关文档来回答用户的问题。"
    "相关文档是：{context}"
    "请根据相关文档来回答用户的问题。"
)
contextualize_q_prompt =ChatPromptTemplate.from_messages([
    {"role":"system","content":contextualize_q_system_prompt},
    {"role":"user","content":query}
])
qa_system_prompt = (
    "你是一个问答助手，你的任务是回答用户的问题。"
    "你需要根据用户的问题和相关文档来回答用户的问题。"
    "相关文档是：{context}"
    "请根据相关文档来回答用户的问题。"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system",qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human","{input}")
])
history_aware_retriever = create_history_aware_retriever(chat,retriever,contextualize_q_prompt)
question_answer_chain = create_stuff_documents_chain(chat,qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

def continual_chat():
    print("\n开始对话吧！")
    chat_history = []
    while True:
        query = input("用户：")
        if query.lower() == "exit":
            break
        result = rag_chain.invoke({"input":query,"chat_history":chat_history})
        print(f"AI:{result['content']}")
        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=result['content']))