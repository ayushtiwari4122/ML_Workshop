import json
import os
from dotenv import load_dotenv
from groq import Groq
from fastmcp import Client

load_dotenv()

# Configuration for groq/LLM Model:::
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

MCP_SERVER_URL = os.getenv(

    "MCP_SERVER_URL",
    "hhtp://127.0.0.1:8001/mcp"
)

# GROQ CLIENT STUP::
groq = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)


# AI AGENT SETUP::
async def ask_agent(question:str):
    async with Client(MCP_SERVER_URL) as client:
        tools = await client.list_tools()

        # CONVERTING TOOL TO GROQ FORMAT
        groq_tools = []
        for tool in tools:
            groq_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameter": tool.inputSchema 
                    }
                }
            )

            # CONVERSTATION / INSTRUCTION FOR LLM::
            messages = [
                {
                    "role":"system",
                    "content": """
YOu are a clincic AI Assistant.
Use MCP tools when the user asks for the doctor or pateint information,
If a tool can answer the question , use that tool
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]

            # GROQ LLM CALLING
            response = groq.chat.completions.create(
                model = GROQ_MODEL,
                messages = messages,
                tools = groq_tools,
                tool_choice = "auto"
            )

            message = response.choice[0].message

            #  IF TOOL NOT NEEDED::
            if not message.tool_calls:
                return{
                "answer": message.content,
                "tool_used": []
                }

            # ADD ASSISTANT TOOL-CALL MESSAGE::
            message.append(
                message.model_dump(
                    exclude_none = True
                )
            )

            # next update  for ai_agent and 10 mcp server making pending