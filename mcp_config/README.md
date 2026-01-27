# MCP Configuration Guide

This directory contains configuration files and examples for integrating the Bitcoin MCP Server with various AI platforms.

## Table of Contents

- [Claude Desktop Configuration](#claude-desktop)
- [Other AI Platforms](#other-ai-platforms)
- [Want to Contribute ?](#want-to-contribute)

---

## Claude Desktop

### Prerequisites

- [Claude Desktop](https://claude.ia/download) installed on your system
- Bitcoin MCP Server downloaded and dependencies installed 

### How to configure ?

Navigate to Bitcoin MCP Server directory and run:

**Using UV (recommended):**
```bash
cd /path/to/bitcoin_mcp
uv run mcp install src/main.py
```

**Using Python:**
```bash
cd /path/to/bitcoin_mcp
python src/main.py mcp install
```

### Verify Installation

1. Launch or restart Claude Desktop (completely close and reopen the application)
2. Sign in with your Anthropic account if prompted
3. Check the MCP connection status:

**✅ Success**: Look in the bottom-right corner of the Claude Desktop chat input bar for a small **"+"** button. Click it and select **"Connectors"**. You should see `bitcoin_mcp_server` listed as a connected server. Make sure the tool is toggled **on** (enabled).

**❌ Error**: If a red pop-up notification appears when launching the app, click **"View Logs"** to see the detailed error message and identify the issue.

### Manual Configuration

If the automatic installation doesn't work, you can manually configure Claude Desktop.

### Configuration File Location

The Claude Desktop configuration file is located at:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

#### Accessing Configuration via Claude Desktop

You can also access the configuration file directly from Claude Desktop:

1. Open **Claude Desktop**
2. Click the **three horizontal lines** (☰) in the top-left corner
3. Select **Settings**
4. Navigate to the **Developer** tab
5. Click **Edit Developer File Configuration** to open the configuration file in your default editor

### Configuration Templates

**Using UV (recommended):** 
```json
{
  "mcpServers": {
    "bitcoin_mcp_server": {
      "command": "absolute/path/to/uv.exe",
      "args": [
        "run",
        "--frozen",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "absolute/path/to/bitcoin_mcp/src/main.py"
      ]
    }
  }
}
```

**Using Python directly:**
```json
{
  "mcpServers": {
    "bitcoin-mcp-server": {
      "command": "absolute/path/to/uv.exe",
      "args": [
        "ABSOLUTE/PATH/TO/bitcoin_mcp/src/main.py"
      ]
    }
  }
}
```

**Important**: Replace all paths with absolute paths to your actual installations. Use forward slashes `/` or escaped backslashes `\\` on Windows.

These files are also available in [claude_desktop_config.json.example](claude_desktop_config.json.example)

## Other AI Platforms

Support for additional AI platforms is coming soon! We're working on configuration guides for:

- ChatGPT
- Google Gemini

## Want to Contribute?

If you've successfully configured the Bitcoin MCP Server with another AI platform, we'd love your contribution! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.