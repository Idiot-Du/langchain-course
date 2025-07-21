import os
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter,SentenceTransformersTokenTextSplitter,TextSplitter,TokenTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import ZhipuAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir,"books","llm.txt")
db_dir = os.path.join(current_dir,"db")

if not os.path.exists(file_path):
    raise FileNotFoundError("文件路径不存在")

loader = TextLoader(file_path,encoding="utf-8")
documents = loader.load()

embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key=os.getenv("ZHIPUAI_API_KEY")
)
def create_vector_store(docs,store_name):
    persistent_dir = os.path.join(db_dir,store_name)
    if not os.path.exists(persistent_dir):
        db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_dir)
        print(f"创建好了{store_name}向量数据库")
    else:
        print(f"{store_name}向量数据库已存在")

print("\n字符分词器")
char_splitter = CharacterTextSplitter(chunk_size=1000)
char_docs = char_splitter.split_documents(documents)
create_vector_store(char_docs,"chroma_db_char")

print("\n句子分割器")
sent_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1000)
sent_docs = sent_splitter.split_documents(documents)
create_vector_store(sent_docs,"chroma_db_sent")

print("\ntoken分词器")
token_splitter = TokenTextSplitter(chunk_size=1000)
token_docs = token_splitter.split_documents(documents)
create_vector_store(token_docs,"chroma_db_token")

print("\n自然地分割器")
rec_char_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
rec_char_docs = rec_char_splitter.split_documents(documents)
create_vector_store(rec_char_docs,"chroma_db_rec_char")

print("\n自制分割器")
class CustomTextSplitter(TextSplitter):
    def split_text(self,text):
        return text.split("\n\n")

custom_splitter = CustomTextSplitter()
custom_docs = custom_splitter.split_documents(documents)
create_vector_store(custom_docs,"chroma_db_custom")

def query_vector_store(store_name,query):
    persistent_dir = os.path.join(db_dir,store_name)
    if os.path.exists(persistent_dir):
        print(f"正在查询向量库{store_name}")
        db = Chroma(persist_directory=persistent_dir,embedding_function=embeddings)
        
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

query = "什么是大语言模型？"

query_vector_store("chroma_db_custom",query)
query_vector_store("chroma_db_rec_char",query)
query_vector_store("chroma_db_sent",query)
query_vector_store("chroma_db_token",query)
query_vector_store("chroma_db_char",query)

