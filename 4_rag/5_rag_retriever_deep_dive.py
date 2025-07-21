import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_community.embeddings import ZhipuAIEmbeddings

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir,"db")
persistent_dir = os.path.join(db_dir,"chroma_db_with_metadata")

embedding = ZhipuAIEmbeddings(
    model = "embedding-3",
    api_key = os.getenv("ZHIPUAI_API_KEY"),
)
db = Chroma(persist_directory=persistent_dir,embedding_function=embedding)

def query_vector_store(store_name,query,embedding_function,search_type,search_kwargs):
    if os.path.exists(persistent_dir):
        print(f"\n从{store_name}向量数据库中查询")
        db = Chroma(
            persist_directory=persistent_dir,
            embedding_function=embedding_function,
        )
        retriever = db.as_retriever(
            search_type = search_type,
            search_kwargs = search_kwargs
        )
        relevant_docs = retriever.invoke(query)
        print(f"\n在{store_name}中找到相关文档")
        for i,doc in enumerate(relevant_docs,1):
            print(f"文档{i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"source:{doc.metadata.get('source','unknow')}\n")
    else:
        print(f"{store_name}向量数据库不存在")

query = "他看到了什么奇怪的现象？"

print("\n使用简单检索")
query_vector_store("chroma_db_with_metadata",query,embedding,"similarity",{"k":1})

print("\n使用最相关的检索")
query_vector_store("chroma_db_with_metadata",query,embedding,"mmr",{"k":3,"fetch_k":20,"lambda":0.5})

print("\n使用分数检索")
query_vector_store("chroma_db_with_metadata",query,embedding,"similarity_score_threshold",{"k":1,"score_threshold":0.2})

print("成功！")



