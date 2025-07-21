from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnableLambda
import os
from langchain.schema.output_parser import StrOutputParser

# 初始化模型
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  
)

# 主分析提示模板 - 只用于初始分析，不传递给并行分支
initial_analysis_prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是一个人物性格分析专家。请简要介绍此人的基本性格特点。"},
    {"role": "user", "content": "请简要分析{name}的总体性格特点。"}
])

# 优点分析分支
def analyze_pros(name):
    pros_template = ChatPromptTemplate.from_messages([
        {"role": "system", "content": "你是一个人物性格分析专家。请详细列举此人性格中的优点。"},
        {"role": "user", "content": "请列举{name}性格中的优点，要求详细具体。"}
    ])
    return pros_template | model | StrOutputParser()

# 缺点分析分支
def analyze_cons(name):
    cons_template = ChatPromptTemplate.from_messages([
        {"role": "system", "content": "你是一个人物性格分析专家。请简要列举此人性格中的不足。"},
        {"role": "user", "content": "请列举{name}性格中的不足，要求简明扼要。"}
    ])
    return cons_template | model | StrOutputParser()

# 合并结果函数
def combine_pros_cons(results):
    return (
        f"总体性格分析:\n{results['initial_analysis']}\n\n"
        f"优点分析:\n{results['pros']}\n\n"
        f"缺点分析:\n{results['cons']}"
    )

# 主分析链 - 只做初始分析
initial_chain = initial_analysis_prompt | model | StrOutputParser()

# 并行分析链 - 接收原始输入字典
parallel_analysis = RunnableParallel({
    "initial_analysis": initial_chain,
    "pros": RunnableLambda(lambda x: analyze_pros(x["name"]).invoke({"name": x["name"]})),
    "cons": RunnableLambda(lambda x: analyze_cons(x["name"]).invoke({"name": x["name"]}))
})

# 完整分析链
chain = parallel_analysis | RunnableLambda(combine_pros_cons)

# 执行分析
result = chain.invoke({"name": "特朗普"})
print(result)