# YNAB MCP Server

[![smithery badge](https://smithery.ai/badge/@EthanKang1/ynab-mcp)](https://smithery.ai/server/@EthanKang1/ynab-mcp)

A Model Context Protocol (MCP) server for interacting with YNAB (You Need A Budget). Provides tools for accessing budget data through MCP-enabled clients like Claude Desktop.

## MCP Client Configuration

### Basic Configuration
Add this to your MCP client's configuration (e.g. `cline_mcp_settings.json` for Claude Desktop):

```json
{
  "mcpServers": {
    "ynab-mcp": {
      "command": "uvx",
      "args": ["run", "ynab-mcp"],
      "env": {
        "YNAB_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Advanced Configuration
If you're running from a specific directory:

```json
{
  "mcpServers": {
    "ynab-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/ynab-mcp", "run", "ynab-mcp"],
      "env": {
        "YNAB_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Debugging
To debug with the MCP Inspector:

1. Install the inspector:
```bash
npm install -g @modelcontextprotocol/inspector
```

2. Update your configuration to use the inspector with uv:
```json
{
  "mcpServers": {
    "ynab-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/ynab-mcp", "run", "@modelcontextprotocol/inspector", "ynab-mcp"],
      "env": {
        "YNAB_API_KEY": "your-api-key-here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

The inspector provides:
- Real-time logs of tool calls and responses
- Request/response inspection
- Tool schema validation
- Interactive testing interface

## Available Tools

### GetUser
Retrieves information about the authenticated YNAB user, including user ID and email.

### ListBudgets
Lists all budgets accessible to the authenticated user, including budget IDs and names.

### GetBudget
Retrieves detailed information about a specific budget, including transactions, categories, and balances. Supports optional date filtering and transaction limiting.

Note: Monetary amounts are returned in milliunits (e.g., 1000 = $1.00)

### GetBudgetCategories
Retrieves all categories defined in the specified budget, including category groups, names, and IDs.

### GetBudgetSettings
Retrieves settings for the specified budget, including currency format, date format, and other preferences.
