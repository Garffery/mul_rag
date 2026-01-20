from langchain_deepseek import ChatDeepSeek

from agent.output_model import Act
from agent.prompts import REPLANNER_PROMPT

replanner = REPLANNER_PROMPT | ChatDeepSeek(
    model="deepseek-chat", temperature=0
).with_structured_output(Act)


