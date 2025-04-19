import os
from typing import Any, Optional

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
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (client-side filter)",
                        "default": "current_month_start"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (client-side filter)",
                        "default": "current_month_end"
                    }
                },
                "required": ["budget_id"]
            },
        )
    
    async def call(self, budget_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[TextContent]:
        await client.connect()
        try:
            result = await client.get_budget(budget_id)
            budget = result['data']['budget']
            
            # Extract essential info
            essential_info = {
                'id': budget['id'],
                'name': budget['name'],
                'currency_format': budget.get('currency_format', {}),
                'time_period': f"{start_date or 'start'} to {end_date or 'end'}",
                'categories': budget.get('categories', {})
            }
            
            # Client-side time filtering of transactions
            if 'transactions' in budget:
                filtered_transactions = [
                    t for t in budget['transactions']
                    if (not start_date or t['date'] >= start_date) and
                       (not end_date or t['date'] <= end_date)
                ]
                essential_info['transactions_count'] = len(filtered_transactions)
                essential_info['transactions'] = filtered_transactions[:10]  # Limit to first 10 transactions
                if len(filtered_transactions) > 10:
                    essential_info['note'] = f"Showing first 10 of {len(filtered_transactions)} transactions in time period"
            
            return [TextContent(
                type="text",
                text=f"Budget Details: {essential_info}"
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
