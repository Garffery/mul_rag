import asyncio

from langchain.agents import create_agent
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek

from agent.output_model import PlanExecute, Response
from agent.planner_agent import planner
from agent.replanner_agent import replanner
from langgraph.graph import END
from langgraph.graph import StateGraph, START
from tools.generate_tools import generate_md



# Choose the LLM that will drive the agent
tools = [TavilySearchResults(max_results=3), generate_md]
llm = ChatDeepSeek(model="deepseek-chat")
prompt = "You are a helpful assistant."
agent_executor = create_agent(llm, tools, system_prompt=prompt)
async def execute_step(state: PlanExecute):
    plan = state["plan"]
    if len(plan) != 0:
        plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""For the following plan:
        {plan_str}\n\nYou are tasked with executing step {1}, {task}."""
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": [(task, agent_response["messages"][-1].content)],
        }
    else:
        return {
            "past_steps": [("", "")],
        }


async def plan_step(state: PlanExecute):
    plan = await planner.ainvoke({"messages": [("user", state["input"])]})
    return {"plan": plan.steps,"aaaa":"测试"}


async def replan_step(state: PlanExecute):
    print(f"replanner规划节点的老的的输出{state}")
    output = await replanner.ainvoke(state)
    print(f"replanner规划节点的新的输出{output}")
    if isinstance(output.action, Response):
        return {"response": output.action.response}
    else:
        return {"plan": output.action.steps}

def should_end(state: PlanExecute):
    if "response" in state and state["response"]:
        return END
    elif len(state["plan"]) == 0:
        return END
    else:
        print(f"当前未执行的任务：'{state["plan"]}'")
        return "agent"

workflow = StateGraph(PlanExecute)

# Add the plan node
workflow.add_node("planner", plan_step)

# Add the execution step
workflow.add_node("agent", execute_step)

# Add a replan node
workflow.add_node("replan", replan_step)

workflow.add_edge(START, "planner")

# From plan we go to agent
workflow.add_edge("planner", "agent")

# From agent, we replan
workflow.add_edge("agent", "replan")

workflow.add_conditional_edges(
    "replan",
    # Next, we pass in the function that will determine which node is called next.
    should_end,
    ["agent", END],
)

app = workflow.compile()

async def main():
    config = {"recursion_limit": 50}
    # inputs = {"input": "分析恒生科技近一个星期的表现并生成文件"}
    inputs = {"input": "写一个小笑话并生成对应的md文件"}
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print("===============")
                print(v)

asyncio.run(main())