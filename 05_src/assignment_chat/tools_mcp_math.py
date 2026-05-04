# From https://www.reddit.com/r/ClaudeAI/comments/1sceak4/i_built_publicly_host_a_handful_of_mcp_servers/
# https://calculator.caseyjhand.com/mcp 
# MCP Connection docs: https://developers.openai.com/api/docs/guides/tools-connectors-mcp


from langchain.tools import tool
from openai import OpenAI

client = OpenAI()

@tool
def mcp_math(query: str) -> str:
    """
    Use an MCP server for math evaluation, simplification, derivatives, etc.
    """
    resp = client.responses.create(
        model="gpt-4o-mini",
        tools=[
            {
                "type": "mcp",
                "server_label": "caseyjhand",
                "server_description": "Math evaluation, simplification, derivatives",
                "server_url": "https://calculator.caseyjhand.com/mcp",
                "require_approval": "never",
            },
        ],
        input=query,
    )

    return resp.output_text