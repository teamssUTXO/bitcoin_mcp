# Bitcoin MCP Server

A comprehensive Model Context Protocol (MCP) server that brings Bitcoin data and functionality directly to AI assistants like Claude, ChatGPT, and other MCP-compatible platforms.

![Bitcoin](https://img.shields.io/badge/Bitcoin-F7931A?logo=bitcoin&logoColor=white)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
![](https://img.shields.io/badge/spread%20the%20bitcoin%20love%20<3-f00020)

---

## 📋 Table of Contents

- [What is MCP?](#-what-is-mcp)
- [Why Use Bitcoin MCP Server?](#-why-use-bitcoin-mcp-server)
- [Features](#-features)
- [Installation](#-installation)
- [API Information](#-api-information)
- [Use Cases](#-use-cases)
- [Available Tools](#-available-tools)
- [Configuration](#-configuration)
- [Usage Considerations](#-usage-considerations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🤖 What is MCP?

The **Model Context Protocol (MCP)** is an open standard that enables AI assistants to securely connect to external data sources and tools. Think of it as a universal adapter that lets AI models interact with your applications, databases, and APIs in a standardized way.

### Key Benefits of MCP

- **🔌 Plug-and-Play Integration**: Connect AI assistants to external tools without custom code
- **🔒 Secure**: Controlled access to data and operations
- **🌐 Universal**: Works across different AI platforms (Claude, ChatGPT, etc.)
- **📦 Modular**: Easy to add, remove, or update capabilities

Learn more at [modelcontextprotocol.io](https://modelcontextprotocol.io/)

---

## 💡 Why Use Bitcoin MCP Server?

The Bitcoin MCP Server empowers AI assistants with real-time Bitcoin data and analysis capabilities:

- **📊 Real-time Data**: Access current Bitcoin prices, market data, and network statistics
- **🔍 Blockchain Analysis**: Query blocks, transactions, and addresses directly
- **⛏️ Mining Insights**: Get hashrate, difficulty, and mining pool information
- **💰 Market Intelligence**: Track price movements, volume, and market capitalization
- **🌐 Network Health**: Monitor mempool status, fee estimates, and node statistics

**No Bitcoin expertise required** - just ask questions in natural language, and the AI handles the technical queries for you!

---

## ✨ Features

- **Network Overview**: Real-time Bitcoin network statistics including hashrate, difficulty, block production, and transaction volume
- **Transaction Analysis**: Detailed transaction information with input/output breakdown, fee analysis, and confirmation status
- **Address Intelligence**: Complete address analytics including balance, transaction history and UTXO management
- **Block Explorer**: Access to block data with mining pool information, transaction counts, fees, and timestamps
- **Market Data**: Real-time Bitcoin price, market capitalization, trading volume, and multi-timeframe performance analysis
- **Mining Insights**: Top mining pools ranking, hashrate distribution, network dominance statistics, and 3-month historical trends
- **Fee Recommendations**: Dynamic fee estimates for different confirmation speeds (fastest, half-hour, standard, economy)
- **Market Sentiment**: Community sentiment tracking and Fear & Greed Index with 7-day historical data
- **Trending Analytics**: Discover trending cryptocurrencies, NFT collections, and categories

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+** installed on your system
- **UV** package manager (recommended) or **pip**
- An MCP-compatible AI client (e.g., Claude Desktop)

### Option 1: Using UV (Recommended)

UV is a fast Python package installer and resolver.

1. **Install UV** (if not already installed):
```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**:
```bash
   git clone https://github.com/YOUR_USERNAME/bitcoin-mcp-server.git
   cd bitcoin-mcp-server
```

3. **Install dependencies**:
```bash
   uv pip install -e .
```

4. **Install to Claude Desktop**:
```bash
   uv run mcp install src/main.py
```

Check [How to configure MCP Server](mcp_config/README.md)

### Option 2: Using Python/Pip

1. **Clone the repository**:
```bash
   git clone https://github.com/YOUR_USERNAME/bitcoin-mcp-server.git
   cd bitcoin-mcp-server
```

2. **Create a virtual environment** (recommended):
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
   pip install -r requirements.txt
```

4. **Run the server**:
```bash
   python src/main.py
```

### Option 3: Using Docker

See [README.Docker.md](README.Docker.md) for detailed Docker deployment instructions.

---

## 🔑 API Information

### No API Keys Required!

The Bitcoin MCP Server uses **free, public APIs** that don't require authentication or API keys. This makes setup incredibly simple - just install and go!

### Data Sources

The server aggregates data from multiple reliable sources:

- **[Blockchain.com](https://blockchain.com)**
- **[Mempool.space](https://mempool.space)**
- **[CoinGecko](https://coingecko.com)**
- **[Alternative](https://alternative.me/crypto/coins/)**

### Fair Use Policy

While these APIs are free and don't require keys, please use them responsibly:

- ⚠️ **Avoid excessive requests**: Don't spam the APIs with rapid-fire queries
- 🕐 **Rate limiting**: The server implements reasonable delays between requests
- 🤝 **Be respectful**: These services are provided free of charge to the community
- 📊 **Cache when possible**: Results are cached to minimize redundant requests

**Note**: If you plan to use this server at high volume or in a production environment, consider using API keys or self-hosting Bitcoin Core nodes for data access.

---

## 💼 Use Cases

### For Investors & Traders
```
User: "What's the current Bitcoin price and 24-hour trading volume?"
AI: Uses bitcoin_mcp_server to fetch real-time market data from CoinGecko
```
```
User: "Show me the transaction history for address bc1q..."
AI: Retrieves complete transaction history with amounts and timestamps
```

### For Developers & Analysts
```
User: "What's the current network hashrate and mining difficulty?"
AI: Provides real-time mining statistics and difficulty adjustment predictions
```
```
User: "Analyze the last 10 blocks ?"
AI: Fetches block data, miner information, and fee analysis
```

### For Researchers & Educators
```
User: "Explain how Bitcoin mempool works and show me the current status"
AI: Combines educational explanation with live mempool data
```
```
User: "What are the current recommended transaction fees?"
AI: Provides real-time fee recommendations for different priority levels
```

### For Business Intelligence
```
User: "Track Bitcoin's price movement over the last week and identify trends"
AI: Fetches historical data and performs trend analysis
```
```
User: "Compare transaction volumes between the top 5 mining pools"
AI: Aggregates mining pool data and creates comparative analysis
```

---

## 🛠️ Available Tools

The Bitcoin MCP Server provides the following tools organized by category:

### 📬 Address Tools

- `get_address_overview` 
- `get_info_about_address`

### 📦 Block Tools

- `get_10_latest_blocks_informations` 
- `get_block_hash_with_height`
- `get_summary_of_latest_block`

### 💸 Transaction Tools

- `get_bitcoin_transaction_infos`
- `get_transaction_input_output`
- `get_transactions_of_address`

### 💰 Market Tools

- `get_bitcoin_price_usd`
- `get_bitcoin_market_data`
- `get_cryptomarket_overview`
- `get_bitcoin_market_sentiment`
- `get_trending_coins`
- `get_trending_categories`
- `get_trending_nfts`

### ⛏️ Mining Tools

- `get_mining_pools_hashrates_3month`
- `get_top_10_mining_pools_rank`
- `get_bitcoin_network_mining_pools_statistics`
- `get_top1_mining_pool`
- `get_mining_pool_by_slugl`

### 🌐 Network Tools

- `get_bitcoin_network_overview`
- `get_bitcoin_network_recommended_fees`
- `get_bitcoin_network_health`

**Total**: 20+ tools and growing!

For detailed tool documentation, see the inline help in each tool module or use the MCP Inspector.

---

## ⚙️ Configuration

### Quick Setup for Claude Desktop

After installation, configure Claude Desktop to use the Bitcoin MCP Server:
```bash
uv run mcp install src/main.py
```

This command automatically:
- Detects your Claude Desktop installation
- Creates the necessary configuration
- Registers all Bitcoin tools

**Then restart Claude Desktop** to activate the server.

### Manual Configuration

For detailed manual configuration instructions for Claude Desktop and other platforms, see [how to configure MCP Server](mcp_config/README.md).

---

## ⚠️ Usage Considerations

### Message Limits

Using MCP servers **will consume more tokens** from your AI assistant's message allowance because:

- Each tool call requires additional context to be sent
- Results from APIs add to the total token count
- Complex queries may require multiple tool calls

**Impact**: You may reach your daily message limit faster when using Bitcoin MCP tools extensively.

### Rate Limiting

While the APIs are free, rate limits apply. Intensive usage may result in temporary blocks. Please refer to the client website for specific API usage limits.



---

## 🗺️ Roadmap

### Coming Soon

- **Unit Tests**: Comprehensive test coverage for reliability
- **More Platforms**: ChatGPT, Gemini, and other MCP client configurations
- **Specialized Tools**: Domain-specific tools for trading, analytics, and research
- **Enhanced Data Processing**: Improved caching, formatting, and response quality

### Long-term Vision

- **Complete Bitcoin Stack**: Full-featured support for all Bitcoin layers and protocols
- **Specialized Tool Categories**: Expand with domain-specific tools (trading analysis, on-chain metrics, educational resources, technical indicators, etc.)
- **Enterprise-Grade Infrastructure**: Custom Bitcoin Core node integration with advanced caching and performance optimization
- **Real-Time Data Streams**: WebSocket support for live price updates, mempool monitoring, and block notifications
- **Community-Driven Development**: Open governance model with transparent roadmap and regular community input

**Want to help shape the roadmap?** See [CONTRIBUTING.md](CONTRIBUTING.md)!

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated ❤️.

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with MCP Inspector
5. Commit your changes
6. Push to your branch
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security

For security concerns or vulnerability reports, please see our [Security Policy](SECURITY.md).

---

For any questions send me a message on Discord : `teamsutxo`

This project was not vibe-coded.