import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.embeddings import ZhipuAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir,"db","chroma_db")

embeddings = ZhipuAIEmbeddings(
    model = "embedding-3",
    api_key = os.getenv("ZHIPUAI_API_KEY")
)
db = Chroma(persist_directory=persistent_dir,embedding_function=embeddings)

query = "哈利波特怎么了？"

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k":3, "score_threshold": 0.2}
)
relevant_docs = retriever.invoke(query)
print("相关片段:\n")
for i,docs in enumerate(relevant_docs,1):
    print(f"document {i}:\n {docs.page_content}")
    if docs.metadata:
        print(f"source:{docs.metadata.get('source','unknow')}\n")
