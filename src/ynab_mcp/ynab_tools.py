from mcp.types import Tool


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
    
    def call(self):
        raise NotImplementedError("Not implemented yet")
    

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
    
    def call(self):
        raise NotImplementedError("Not implemented yet")

class GetBudgetTool():
    def __init__(self):
        self.name = "GetBudget"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get budget",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    
    def call(self):
        raise NotImplementedError("Not implemented yet")
    
class GetBudgetSettingsTool():
    def __init__(self):
        self.name = "GetBudgetSettings"

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get budget settings",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    
    def call(self):
        raise NotImplementedError("Not implemented yet")
    
## Util methods


def generate_available_tools():
    tools = [GetUserInfoTool(), ListBudgetsTool(), GetBudgetTool(), GetBudgetSettingsTool()]
    return dict((tool.name, tool) for tool in tools)

tools = generate_available_tools()

def get_tool(name: str):
    if name not in tools:
        return None
    
    return tools[name]