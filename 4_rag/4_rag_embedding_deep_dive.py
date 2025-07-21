import os
from dotenv import load_dotenv
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir,"books","llm.txt")
db_dir = os.path.join(current_dir,"db")

if not os.path.exists(file_path):
    raise FileNotFoundError("文件路径不存在")

loader = TextLoader(file_path,encoding="utf-8")
documents = loader.load()

zhipuai_embedding_3 = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key = os.getenv("ZHIPUAI_API_KEY"),
)

zhipuai_embedding_2 = ZhipuAIEmbeddings(
    model="embedding-2",
    api_key = os.getenv("ZHIPUAI_API_KEY"),
)
def create_vector_store(docs,embeddings,store_name):
    persistent_dir = os.path.join(db_dir,store_name)
    if not os.path.exists(persistent_dir):
        db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_dir)
        print(f"创建好了{store_name}向量数据库")
    else:
        print(f"{store_name}向量数据库已存在")

text_splitter = CharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(documents)

print("\nembedding-3模型")
create_vector_store(docs,zhipuai_embedding_3,"chroma_db_zhipuai_3")

print("\nembedding-2模型")
create_vector_store(docs,zhipuai_embedding_2, "chroma_db_zhipuai_2")

query = "大模型是什么"
def query_vector_store(store_name,query,embedding_function):
    persistent_dir = os.path.join(db_dir,store_name)
    if os.path.exists(persistent_dir):
        print(f"正在查询向量库{store_name}")
        db = Chroma(persist_directory=persistent_dir,embedding_function=embedding_function)
        retriever = db.as_retriever(
            search_type = "similarity_score_threshold",
            search_kwargs = {"k":1,"score_threshold":0.2}
        )
        relevant_docs = retriever.invoke(query)
        print(f"\n在{store_name}中找到相关文档")
        for i,doc in enumerate(relevant_docs,1):
            print(f"文档{i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"source:{doc.metadata.get('source','unknow')}\n")
    else:
        print(f"{store_name}向量数据库不存在")

query_vector_store("chroma_db_zhipuai_3",query,zhipuai_embedding_3)
query_vector_store("chroma_db_zhipuai_2",query,zhipuai_embedding_2)

print("结束！")
