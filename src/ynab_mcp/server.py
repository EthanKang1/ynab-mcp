import asyncio

import os

import logging
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from . import ynab_tools

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("ynab-mcp")

# Get YNAB API key
api_key = os.getenv("YNAB_API_KEY")
if not api_key:
    raise ValueError(f"YNAB_API_KEY environment variable required. Working directory: {os.getcwd()}")

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server("ynab-mcp")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    raise NotImplementedError("Not implemented yet.")
    # return [
    #     types.Resource(
    #         uri=AnyUrl(f"note://internal/{name}"),
    #         name=f"Note: {name}",
    #         description=f"A simple note named {name}",
    #         mimeType="text/plain",
    #     )
    #     for name in notes
    # ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    raise NotImplementedError("Not implemented yet.")
    # if uri.scheme != "note":
    #     raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    # name = uri.path
    # if name is not None:
    #     name = name.lstrip("/")
    #     return notes[name]
    # raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    raise NotImplementedError("Not implemented yet.")
    # return [
    #     types.Prompt(
    #         name="summarize-notes",
    #         description="Creates a summary of all notes",
    #         arguments=[
    #             types.PromptArgument(
    #                 name="style",
    #                 description="Style of the summary (brief/detailed)",
    #                 required=False,
    #             )
    #         ],
    #     )
    # ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    raise NotImplementedError("Not implemented yet.")
    # if name != "summarize-notes":
    #     raise ValueError(f"Unknown prompt: {name}")

    # style = (arguments or {}).get("style", "brief")
    # detail_prompt = " Give extensive details." if style == "detailed" else ""

    # return types.GetPromptResult(
    #     description="Summarize the current notes",
    #     messages=[
    #         types.PromptMessage(
    #             role="user",
    #             content=types.TextContent(
    #                 type="text",
    #                 text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
    #                 + "\n".join(
    #                     f"- {name}: {content}"
    #                     for name, content in notes.items()
    #                 ),
    #             ),
    #         )
    #     ],
    # )

tools = ynab_tools.tools

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """

    return [t.get_tool_description() for t in tools.values()]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """

    tool = ynab_tools.get_tool(name)
    if not tool:
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        if arguments:
            return await tool.call(**arguments)
        return await tool.call()
    except Exception as e:
        logger.error(str(e))
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ynab-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
