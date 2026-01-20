from langchain_deepseek import ChatDeepSeek
from config import Mul_Agent_Config
from prompts import PLANNER_PROMPT
from output_model import Plan
model_name = Mul_Agent_Config.planner_model_name


llm = ChatDeepSeek(model="deepseek-chat")

planner = PLANNER_PROMPT | ChatDeepSeek(
    model="deepseek-chat", temperature=0
).with_structured_output(Plan)
