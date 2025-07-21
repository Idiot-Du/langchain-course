import os
from dotenv import load_dotenv
from langchain.text_splitter import TextSplitter,RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_community.embeddings import ZhipuAIEmbeddings

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir,"db")
persistent_dir = os.path.join(db_dir,"chroma_db_web")

urls = ["https://baike.baidu.com/item/%E7%AB%A0%E9%B1%BC/77798"]

loader = WebBaseLoader(urls)
documents = loader.load()  

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
docs = text_splitter.split_documents(documents)

print("------------文件信息-------------")
print(f"\n number of document chunks:{len(docs)}")
print(docs[0].page_content)
print(docs)

embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key=os.getenv("ZHIPUAI_API_KEY")
)
if not os.path.exists(persistent_dir):
    db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_dir)
    print(f"创建好了chroma_db_web向量数据库")
else:
    db = Chroma(persist_directory=persistent_dir,embedding_function=embeddings)

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs = {"k":1,"score_threshold":0.2}
)

query = "章鱼的生长环境？"
relevant_docs = retriever.invoke(query)

for i,docs in enumerate(relevant_docs,1):
    print(f"文档{i}:\n{docs.page_content}\n")
