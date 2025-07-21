from langchain import hub
from langchain.agents import AgentExecutor,create_react_agent
from langchain_core.tools import Tool
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os
load_dotenv()

def get_current_time(*args,**kwargs):
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

tools = [
    Tool(
        name = "Time",
        func = get_current_time,
        description="useful when you want to know the current time"
    )
]

prompt = hub.pull("hwchase17/react")
llm = ChatDeepSeek(
    model = "deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

agent = create_react_agent(
    llm = llm,
    tools = tools,
    prompt = prompt,
    stop_sequence = True
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)
response = agent_executor.invoke({"input":"你好,现在是什么时间？"})
print(response)