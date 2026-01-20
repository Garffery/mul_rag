from pydantic import BaseModel, Field
from typing import List, Union, Literal
import operator
from typing_extensions import TypedDict
from typing import Annotated, List, Tuple

class Plan(BaseModel):
    """规划器输出结果格式"""
    type: Literal["steps"] = "steps"
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )


class Response(BaseModel):
    """Response to user."""
    type: Literal["response"] = "response"
    response: str

class Act(BaseModel):
    """执行器输出格式"""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


class PlanExecute(TypedDict):
    """agent状态"""
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str