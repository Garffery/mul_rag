import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field



class MdInput(BaseModel):
    content: str = Field(..., description="符合markdown语法的字符串")
    path: str = Field(..., description="生成的文件路径")
    file_name: str =  Field(..., description="文件名称")

@tool(args_schema=MdInput)
def generate_md(content:str, path:str, file_name:str) -> str:
    """根据传入的content生成对应的markdown文件"""
    final_path = path + file_name + ".md"
    os.makedirs(os.path.dirname(final_path), exist_ok=True)
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(content)


generate_md.run({"content":"# aaa","path":"./tmp/", "file_name":"name"})