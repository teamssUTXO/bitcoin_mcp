# Bitcoin MCP Server

A comprehensive Model Context Protocol (MCP) server that brings Bitcoin data and functionality directly to AI assistants like Claude, ChatGPT, and other MCP-compatible platforms.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

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

### Core Capabilities

- **Address Operations**: Check balances, UTXOs, and transaction history for any Bitcoin address
- **Block Explorer**: Retrieve block details, transactions, and mining information
- **Transaction Analysis**: Get transaction details, status, and fee information
- **Market Data**: Real-time and historical price data from multiple sources
- **Mining Statistics**: Hashrate, difficulty adjustments, and pool distribution
- **Network Metrics**: Mempool status, fee recommendations, and network health
- **Multi-API Support**: Aggregates data from Blockchain.com, Mempool.space, CoinGecko, and more

### Technical Features

- 🚀 **Fast & Lightweight**: Efficient data retrieval with minimal overhead
- 🛡️ **Type-Safe**: Built with Python dataclasses for reliability
- 📝 **Well-Documented**: Comprehensive inline documentation and examples
- 🧪 **Tested**: Unit tests to ensure code quality (expanding coverage)
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 🔧 **Configurable**: Flexible configuration via environment variables

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

- `get_info_about_address`: 
- `get_address_overview`: 

### 📦 Block Tools

- `get_10_latest_blocks_informations`: 
- `get_block_hash_with_height`: 
- `get_summary_of_latest_block`: 

### 💸 Transaction Tools

- `get_bitcoin_transaction_infos`: 
- `get_transaction_input_output`: 
- `get_transactions_of_address`: 

### 💰 Market Tools

- `get_bitcoin_price_usd`: 
- `get_bitcoin_market_data`: 
- `get_cryptomarket_overview`: 
- `get_bitcoin_market_sentiment`:
- `get_trending_coins`: 
- `get_trending_categories`: 
- `get_trending_nfts`: 

### ⛏️ Mining Tools

- `get_mining_pools_hashrates_3month`: 
- `get_top_10_mining_pools_rank`: 
- `get_bitcoin_network_mining_pools_statistics`: 
- `get_top1_mining_pool`: 
- `get_mining_pool_by_slug`: 

### 🌐 Network Tools

- `get_bitcoin_network_overview`: Current mempool size and transaction count
- `get_bitcoin_network_recommended_fees`: General Bitcoin network statistics
- `get_bitcoin_network_health`: Number of reachable nodes on the network

**Total**: 25+ tools and growing!

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

For detailed manual configuration instructions for Claude Desktop and other platforms, see [mcp_config/README.md](mcp_config/README.md).

### Environment Variables

Create a `.env` file in the project root (optional):
```bash
# Logging
LOG_LEVEL=INFO

# API Configuration (if using authenticated endpoints)
BLOCKCHAIN_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here

# Bitcoin Node (optional - for direct node access)
BITCOIN_RPC_URL=http://localhost:8332
BITCOIN_RPC_USER=your_user
BITCOIN_RPC_PASSWORD=your_password
```

Most users won't need to configure anything - the defaults work great!

---

## ⚠️ Usage Considerations

### Message Limits

Using MCP servers **will consume more tokens** from your AI assistant's message allowance because:

- Each tool call requires additional context to be sent
- Results from APIs add to the total token count
- Complex queries may require multiple tool calls

**Impact**: You may reach your daily message limit faster when using Bitcoin MCP tools extensively.

**Tips to optimize**:
- Ask focused questions rather than broad explorations
- Limit the number of addresses/transactions queried at once
- Use summary requests instead of detailed breakdowns when possible

### Rate Limiting

While the APIs are free, they may implement rate limiting:

- **Blockchain.com**: ~1 request per second recommended
- **Mempool.space**: Generally permissive, but avoid abuse
- **CoinGecko**: 10-50 calls/minute on free tier

The server implements basic rate limiting to prevent issues, but very intensive use may encounter temporary blocks.

---

## 🗺️ Roadmap

### Coming Soon

- ⚡ **Layer 2 Support**: Lightning Network data and statistics
- 🌊 **Liquid Network**: Liquid sidechain tools and asset tracking
- 🔧 **Additional Platforms**: Configuration guides for ChatGPT, Gemini, and more
- 🧪 **Comprehensive Tests**: Expanded unit and integration test coverage
- 📊 **Advanced Analytics**: On-chain analytics and pattern recognition
- 🔔 **Alert System**: Price alerts and transaction monitoring
- 📈 **Historical Analysis**: Deep-dive into historical blockchain data

### Long-term Vision

- Support for other cryptocurrencies (Ethereum, Litecoin, etc.)
- Custom node integration for enterprise users
- Advanced charting and visualization tools
- WebSocket support for real-time updates

**Want to help shape the roadmap?** See [CONTRIBUTING.md](CONTRIBUTING.md)!

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test with MCP Inspector
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security

For security concerns or vulnerability reports, please see our [Security Policy](SECURITY.md).

**Do not** create public GitHub issues for security vulnerabilities.

---

## 📞 Support

- **Documentation**: Check this README and [mcp_config/README.md](mcp_config/README.md)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Discord**: Message `teamsutxo` for questions

---

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for creating Claude and the MCP protocol
- [Blockchain.com](https://blockchain.com), [Mempool.space](https://mempool.space), and [CoinGecko](https://coingecko.com) for their excellent free APIs
- The Bitcoin community for continued innovation and support
- All contributors who help make this project better

---

## 📝 Final Note

**This code was not vibe-coded.** Every line was thoughtfully crafted, tested, and documented to provide a reliable, professional tool for the Bitcoin and AI communities. 

---

**Star ⭐ this repository** if you find it useful!

**Let's bring Bitcoin to AI, together!** 🚀⚡

=========================================

[//]: # (TODO : )
MCP Inspector : 

Erreur lors de la connexion HTTP sans proxy. Le message ne prend pas en compte si on utilise le proxy ou non. copier-coller pas très bien formatté.  
Faire dynamiquement le fait que si on choisit SSE, ça mette /sse, et si on met http, ça met /mcp en endpoint de connexion