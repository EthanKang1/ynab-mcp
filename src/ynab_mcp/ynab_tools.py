import os
from typing import Any

from mcp.types import ImageContent, TextContent, Tool

from .ynab_client import YNABClient

# Initialize YNAB client
api_key = os.getenv("YNAB_API_KEY")
if not api_key:
    raise ValueError("YNAB_API_KEY environment variable is required")

client = YNABClient(api_key)

### User
class GetUserInfoTool():
    def __init__(self):
        self.name = "GetUser"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="User info",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    
    async def call(self) -> list[TextContent]:
        await client.connect()
        try:
            result = await client.get_user()
            return [TextContent(
                type="text",
                text=f"User Info: {result['data']['user']}"
            )]
        finally:
            await client.close()

## Budgets
class ListBudgetsTool():
    def __init__(self):
        self.name = "ListBudgets"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List budgets",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    
    async def call(self) -> list[TextContent]:
        await client.connect()
        try:
            result = await client.list_budgets()
            return [TextContent(
                type="text",
                text=f"Budgets: {result['data']['budgets']}"
            )]
        finally:
            await client.close()

class GetBudgetTool():
    def __init__(self):
        self.name = "GetBudget"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The ID of the budget to fetch"
                    }
                },
                "required": ["budget_id"]
            },
        )
    
    async def call(self, budget_id: str) -> list[TextContent]:
        await client.connect()
        try:
            result = await client.get_budget(budget_id)
            return [TextContent(
                type="text",
                text=f"Budget Details: {result['data']['budget']}"
            )]
        finally:
            await client.close()
    
class GetBudgetSettingsTool():
    def __init__(self):
        self.name = "GetBudgetSettings"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get budget settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The ID of the budget to fetch settings for"
                    }
                },
                "required": ["budget_id"]
            },
        )
    
    async def call(self, budget_id: str) -> list[TextContent]:
        await client.connect()
        try:
            result = await client.get_budget_settings(budget_id)
            return [TextContent(
                type="text",
                text=f"Budget Settings: {result['data']['settings']}"
            )]
        finally:
            await client.close()
    
## Util methods


def generate_available_tools():
    tools = [GetUserInfoTool(), ListBudgetsTool(), GetBudgetTool(), GetBudgetSettingsTool()]
    return dict((tool.name, tool) for tool in tools)

tools = generate_available_tools()

def get_tool(name: str):
    if name not in tools:
        return None
    
    return tools[name]
