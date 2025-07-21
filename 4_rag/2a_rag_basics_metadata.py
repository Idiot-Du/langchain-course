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
book_dir = os.path.join(current_dir,"books")
db_dir = os.path.join(current_dir,"db")
persistent_dir = os.path.join(db_dir,"chroma_db_with_metadata")

print(f"books directory:{book_dir}")
print(f"persistent directory:{persistent_dir}")

if not os.path.exists(persistent_dir):
    print("创建目录")
    os.makedirs(persistent_dir)

    if not os.path.exists(book_dir):
        raise FileNotFoundError(f"文件路径不存在: {book_dir}")
    
    book_files = [f for f in os.listdir(book_dir) if f.endswith(".txt")]

    documents = []
    for book_file in book_files:
        file_path = os.path.join(book_dir,book_file)
        loader = TextLoader(file_path,encoding="utf-8")
        book_docs = loader.load()
        for doc in book_docs:
            doc.metadata = {"source":book_file}
            documents.append(doc)
    
    text_splitter = CharacterTextSplitter(chunk_size=100,chunk_overlap=10)
    docs = text_splitter.split_documents(documents)

    print(f"文件的总块数：{len(docs)}")
    print("创建嵌入向量数据库")

    embeddings = ZhipuAIEmbeddings(
        model = "embedding-3",
        api_key = os.getenv("ZHIPUAI_API_KEY")
    )
    db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_dir)
    print("成功")
else:
    print("向量数据库信息已存在")