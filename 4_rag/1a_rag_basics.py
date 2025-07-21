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
file_path = os.path.join(current_dir,"books","myBooks.txt")
persistent_dir = os.path.join(current_dir,"db","chroma_db")

if not os.path.exists(persistent_dir):
    print("创建目录")
    os.makedirs(persistent_dir)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件路径不存在: {file_path}")
    
    loader = TextLoader(file_path,encoding="utf-8")
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=50,chunk_overlap=10)
    docs = text_splitter.split_documents(documents)
    
    print("\n-----文档切割信息-----")
    print(f"切割后文档数量: {len(docs)}")
    print(f"文档样本: {docs[0].page_content}\n")

    print("\n加载嵌入向量模型信息")
    embeddings = ZhipuAIEmbeddings(
        model = "embedding-3",
        api_key=os.getenv("ZHIPUAI_API_KEY")
    )
    print("嵌入向量模型信息加载完成")

    print("\n创建向量数据库信息")
    vector_db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=persistent_dir
    )
    print("向量数据库信息创建完成")
else:
    print("向量数据库信息已存在")