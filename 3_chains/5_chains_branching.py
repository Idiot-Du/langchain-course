from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableBranch
import os

# 初始化模型
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")  
)

# 情感分类提示模板
classification_template = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是情感分析专家，仅返回'positive'、'negative'或'neutral'中的一个。"},
    {"role": "human", "content": "判断反馈的情感倾向：{feedback}"}
])

# 积极反馈回复模板
positive_template_feedback = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是智能助手，负责生成积极感谢信。"},
    {"role": "human", "content": "回应反馈：{feedback}。以'非常感谢你的反馈！'开头。"}
])

# 消极反馈回复模板
negative_template_feedback = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是智能助手，负责生成消极感谢信。"},
    {"role": "human", "content": "回应反馈：{feedback}。以'非常遗憾收到你的反馈！'开头。"}
])

# 中性反馈回复模板
neutral_template_feedback = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是智能助手，负责生成中性感谢信。"},
    {"role": "human", "content": "回应反馈：{feedback}。以'这样啊……'开头。"}
])

# 情感分类链
classification_chain = classification_template | model | StrOutputParser()

# 定义默认分支（当所有条件不匹配时使用）
default_branch = RunnableLambda(
    lambda x: f"无法识别的情感类型，请检查输入。原始分类结果：{x}"
)

# 分支链：将默认分支作为最后一个位置参数传入
branches = RunnableBranch(
    # 条件1：如果分类结果是positive，使用积极模板
    (lambda x: x.lower().strip() == "positive", positive_template_feedback | model | StrOutputParser()),
    # 条件2：如果分类结果是negative，使用消极模板
    (lambda x: x.lower().strip() == "negative", negative_template_feedback | model | StrOutputParser()),
    # 条件3：如果分类结果是neutral，使用中性模板
    (lambda x: x.lower().strip() == "neutral", neutral_template_feedback | model | StrOutputParser()),
    # 最后一个参数作为默认分支
    default_branch
)

# 完整链：先分类，再根据分类结果选择分支
chain = classification_chain | branches

# 执行链
result = chain.invoke({"feedback": "我今天吃了一碗牛肉面。"})
print(result)