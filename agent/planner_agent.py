from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from config import Mul_Agent_Config

model_name = Mul_Agent_Config.planner_model_name


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

model = init_chat_model(
    model_name,
    temperature=0
)

# model = create_agent(model = model_name)

def chatbot(state: State):
    res = model.invoke(state["messages"])
    print(res)
    print("===============")
    return {"messages": [res]}


graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print(value)
            print("Assistant:", value["messages"][-1].content)


# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input)
#     except:
#         # fallback if input() is not available
#         # user_input = "What do you know about LangGraph?"
#         # print("User: " + user_input)
#         # stream_graph_updates(user_input)
#         print("invalid ----------")
#         break

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)