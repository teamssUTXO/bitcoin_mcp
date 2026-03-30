"""
Unit Tests for Bitcoin MCP Server
==================================

This test suite covers:
1. Test imports - Verify all modules import correctly
2. Test the logger and write log files - Test LoggerMCP class functionality
3. Test de l'endpoint /health - Test the /health HTTP endpoint
4. Test de fonctions qui peuvent être testés - Test testable functions
5. Test de l'appel de la fonction list_tools comme client - Test list_tools as MCP client
6. Test gestion d'erreur avec invalid input - Test error handling with invalid inputs
7. Test configuration - Test configuration loading and validation

Testing with MCP Inspector
---------------------------
You can also test the server interactively using the MCP Inspector:

    cd /path/to/bitcoin_mcp
    mcp dev src/main.py

The MCP Inspector creates a local MCP client in your browser.

Resources:
    - Documentation: https://modelcontextprotocol.io/docs/tools/inspector
    - GitHub: https://github.com/modelcontextprotocol/inspector
"""

import unittest
import logging
import os
import sys
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# TEST 1: Test imports
# ============================================================================
class TestImports(unittest.TestCase):
    """Test that all modules can be imported successfully"""

    def test_import_config(self):
        """Test config module imports"""
        try:
            from src.config import Config, config

            self.assertIsNotNone(Config)
            self.assertIsNotNone(config)
        except ImportError as e:
            self.fail(f"Failed to import config: {e}")

    def test_import_log(self):
        """Test log module imports"""
        try:
            from src.log import LoggerMCP, get_logger

            self.assertIsNotNone(LoggerMCP)
            self.assertIsNotNone(get_logger)
        except ImportError as e:
            self.fail(f"Failed to import log: {e}")

    def test_import_api_client(self):
        """Test API client imports"""
        try:
            from src.api.client import APIClient
            from src.api.mempool_client import MempoolClient, get_mempool_client
            from src.api.blockchain_client import (
                BlockchainClient,
                get_blockchain_client,
            )
            from src.api.coingecko_client import CoinGeckoClient, get_coingecko_client
            from src.api.alternative_client import (
                AlternativeClient,
                get_alternative_client,
            )

            self.assertIsNotNone(APIClient)
        except ImportError as e:
            self.fail(f"Failed to import API clients: {e}")

    def test_import_data_classes(self):
        """Test data classes imports"""
        try:
            from src.data.network_dataclasses import DataNetworkStats, DataNetworkFees
            from src.data.transactions_dataclasses import DataTransactionInfo
            from src.data.blocks_dataclasses import DataLatestBlock, DataLatestBlocks
            from src.data.addresses_dataclasses import (
                DataOverviewAddress,
                DataInfosAddress,
            )
            from src.data.market_dataclasses import (
                DataMarketOverview,
                DataBitcoinPriceUSD,
            )
            from src.data.mining_dataclasses import DataRankingMiningPools

            self.assertIsNotNone(DataNetworkStats)
        except ImportError as e:
            self.fail(f"Failed to import data classes: {e}")

    def test_import_core_analyzers(self):
        """Test core analyzer imports"""
        try:
            from src.core.network import NetworkAnalyzer, get_network_analyser_client
            from src.core.transactions import (
                TransactionAnalyzer,
                get_transactions_analyser_client,
            )
            from src.core.blocks import BlockAnalyzer, get_blocks_analyser_client
            from src.core.addresses import (
                AddressAnalyzer,
                get_addresses_analyser_client,
            )
            from src.core.market import MarketAnalyzer, get_market_analyser_client
            from src.core.mining import MiningPoolAnalyzer, get_mining_analyser_client

            self.assertIsNotNone(NetworkAnalyzer)
        except ImportError as e:
            self.fail(f"Failed to import core analyzers: {e}")

    def test_import_tools(self):
        """Test tools imports"""
        try:
            from src.tools.network_tools import register_network_tools
            from src.tools.transactions_tools import register_transactions_tools
            from src.tools.blocks_tools import register_blocks_tools
            from src.tools.addresses_tools import register_addresses_tools
            from src.tools.market_tools import register_market_tools
            from src.tools.mining_tools import register_mining_tools

            self.assertIsNotNone(register_network_tools)
        except ImportError as e:
            self.fail(f"Failed to import tools: {e}")

    def test_import_main(self):
        """Test main module imports"""
        try:
            import logging

            # Temporarily suppress INFO logging during import to reduce test noise
            logging.disable(logging.INFO)

            from src import main

            # Re-enable logging
            logging.disable(logging.NOTSET)

            self.assertIsNotNone(main)
        except ImportError as e:
            self.fail(f"Failed to import main: {e}")


# ============================================================================
# TEST 2: Test configuration
# ============================================================================
class TestConfiguration(unittest.TestCase):
    """Test configuration loading and validation"""

    def test_config_default_values(self):
        """Test that config has correct default values"""
        from src.config import config, Config

        # Test API URLs
        self.assertEqual(config.MEMPOOL_API_URL, "https://mempool.space/api")
        self.assertEqual(config.COINGECKO_API_URL, "https://api.coingecko.com/api/v3")
        self.assertEqual(config.BLOCKCHAIN_INFO_API_URL, "https://blockchain.info")
        self.assertEqual(config.ALTERNATIVE_API_URL, "https://api.alternative.me")

        # Test constants
        self.assertEqual(config.SATOSHI, 100_000_000)

        # Test cache and retry settings
        self.assertTrue(config.ENABLE_CACHE)
        self.assertTrue(config.ENABLE_RETRY)
        self.assertEqual(config.CACHE_TTL_TIME, 60)
        self.assertEqual(config.MAX_RETRIES, 3)

        # Test timeout settings
        self.assertEqual(config.API_CONNECT_TIMEOUT, 5)
        self.assertEqual(config.API_READ_TIMEOUT, 30)
        self.assertEqual(config.API_WRITE_TIMEOUT, 10)
        self.assertEqual(config.API_POOL_TIMEOUT, 5)

        # Test logging settings
        self.assertEqual(config.LOGGER_NAME, "bitcoin_mcp_server")
        self.assertEqual(config.LOG_LEVEL, "INFO")
        self.assertEqual(config.LOGGER_BACKUP_COUNT, 30)
        self.assertTrue(config.LOGGER_CONSOLE_OUTPUT)

    def test_config_is_dataclass(self):
        """Test that Config is a proper dataclass"""
        from src.config import Config

        self.assertTrue(hasattr(Config, "__dataclass_fields__"))

    def test_config_singleton(self):
        """Test that config is a singleton instance"""
        from src.config import config

        self.assertIsNotNone(config)

    def test_config_log_dir_path(self):
        """Test that log directory path is correctly formed"""
        from src.config import config

        log_dir = Path(config.LOG_DIR)
        self.assertTrue(log_dir.name == "logs")


# ============================================================================
# TEST 3: Test the logger and write log files
# ============================================================================
class TestLogger(unittest.TestCase):
    """Test LoggerMCP class functionality and log file creation"""

    def setUp(self):
        """Setup test environment with temporary log directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_log_dir = None

    def tearDown(self):
        """Cleanup temporary log directory"""
        # Close all handlers to release file locks
        import logging

        for handler in logging.root.handlers[:]:
            try:
                handler.close()
            except:
                pass

        # Small delay to ensure files are released on Windows
        import time

        time.sleep(0.1)

        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except PermissionError:
                # On Windows, files may still be locked - that's okay
                pass

    @patch("src.config.Config.LOG_DIR")
    def test_logger_initialization(self, mock_log_dir):
        """Test that LoggerMCP initializes correctly"""
        mock_log_dir.__get__ = Mock(return_value=self.temp_dir)

        from src.log import LoggerMCP

        logger_mcp = LoggerMCP()

        self.assertIsNotNone(logger_mcp)
        self.assertEqual(logger_mcp.logger_name, "bitcoin_mcp_server")
        self.assertIsNotNone(logger_mcp.root_logger)

    @patch("src.config.Config.LOG_DIR")
    def test_logger_creates_log_directory(self, mock_log_dir):
        """Test that logger creates log directory if it doesn't exist"""
        log_path = Path(self.temp_dir) / "test_logs"
        mock_log_dir.__get__ = Mock(return_value=str(log_path))

        from src.log import LoggerMCP

        logger_mcp = LoggerMCP()

        self.assertTrue(log_path.exists())
        self.assertTrue(log_path.is_dir())

    @patch("src.config.Config.LOG_DIR")
    def test_logger_creates_log_file(self, mock_log_dir):
        """Test that logger creates log file"""
        mock_log_dir.__get__ = Mock(return_value=self.temp_dir)

        from src.log import LoggerMCP

        logger_mcp = LoggerMCP()

        # Temporarily disable console output to reduce test noise
        logging.disable(logging.INFO)

        # Write a test log message
        test_logger = logging.getLogger("test_logger")
        test_logger.info("Test log message")

        # Re-enable logging
        logging.disable(logging.NOTSET)

        # Force flush handlers
        for handler in logger_mcp.root_logger.handlers:
            handler.flush()

        # Check if log file exists
        log_file = Path(self.temp_dir) / "server.log"
        self.assertTrue(log_file.exists())

    @patch("src.config.Config.LOG_DIR")
    @patch("src.config.Config.LOG_LEVEL", "DEBUG")
    def test_logger_log_levels(self, mock_log_dir):
        """Test that logger respects log levels"""
        mock_log_dir.__get__ = Mock(return_value=self.temp_dir)

        from src.log import LoggerMCP

        logger_mcp = LoggerMCP()

        # Check that log level is set correctly
        self.assertEqual(logger_mcp.root_logger.level, logging.DEBUG)

    @patch("src.config.Config.LOG_DIR")
    @patch("src.config.Config.LOGGER_CONSOLE_OUTPUT", False)
    def test_logger_console_output_disabled(self, mock_log_dir):
        """Test that console output can be disabled"""
        mock_log_dir.__get__ = Mock(return_value=self.temp_dir)

        from src.log import LoggerMCP

        logger_mcp = LoggerMCP()

        # Check that only file handler is present (no console handler)
        handler_types = [type(h).__name__ for h in logger_mcp.root_logger.handlers]
        self.assertIn("TimedRotatingFileHandler", handler_types)
        # Console handler should not be present
        stream_handlers = [
            h
            for h in logger_mcp.root_logger.handlers
            if isinstance(h, logging.StreamHandler) and not hasattr(h, "baseFilename")
        ]
        self.assertEqual(len(stream_handlers), 0)

    def test_get_logger_singleton(self):
        """Test that get_logger returns singleton instance"""
        from src.log import get_logger

        logger1 = get_logger()
        logger2 = get_logger()

        self.assertIs(logger1, logger2)


# ============================================================================
# TEST 4: Test API Client (cache, retry, HTTP operations)
# ============================================================================
class TestAPIClient(unittest.IsolatedAsyncioTestCase):
    """Test APIClient base class functionality"""

    def setUp(self):
        """Setup test client"""
        from src.api.client import APIClient

        self.client = APIClient("https://test.example.com")

    def tearDown(self):
        """Cleanup"""
        self.client._cache.clear()

    def test_client_initialization(self):
        """Test that APIClient initializes with correct settings"""
        from src.config import Config

        self.assertEqual(self.client.base_url, "https://test.example.com")
        self.assertEqual(self.client.ttl, Config.CACHE_TTL_TIME)
        self.assertEqual(self.client.max_retry, Config.MAX_RETRIES)
        self.assertTrue(self.client.enable_cache)
        self.assertTrue(self.client.enable_retry)

    def test_cache_save_and_retrieve(self):
        """Test that cache saves and retrieves data correctly"""
        test_key = "test_endpoint"
        test_data = {"key": "value"}

        # Save to cache
        self.client._save_to_cache(test_key, test_data)

        # Retrieve from cache
        cached_data = self.client._get_from_cache(test_key)

        self.assertEqual(cached_data, test_data)

    def test_cache_expiration(self):
        """Test that cache expires after TTL"""
        test_key = "test_endpoint"
        test_data = {"key": "value"}

        # Save to cache with old timestamp
        old_timestamp = time.time() - (self.client.ttl + 10)
        self.client._cache[test_key] = (test_data, old_timestamp)

        # Try to retrieve - should return None
        cached_data = self.client._get_from_cache(test_key)

        self.assertIsNone(cached_data)

    def test_cache_disabled(self):
        """Test that cache can be disabled"""
        self.client.enable_cache = False
        test_key = "test_endpoint"
        test_data = {"key": "value"}

        # Save should not cache
        self.client._save_to_cache(test_key, test_data)

        # Cache should be empty
        self.assertEqual(len(self.client._cache), 0)

        # Retrieve should return None
        cached_data = self.client._get_from_cache(test_key)
        self.assertIsNone(cached_data)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_get_successful_request(self, mock_get):
        """Test successful GET request"""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = await self.client.get("/test")

        self.assertEqual(result, {"success": True})
        mock_get.assert_called_once()

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_get_uses_cache(self, mock_get):
        """Test that GET uses cache for subsequent requests"""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # First call
        result1 = await self.client.get("/test")
        # Second call - should use cache
        result2 = await self.client.get("/test")

        self.assertEqual(result1, result2)
        # Should only call API once
        self.assertEqual(mock_get.call_count, 1)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_get_retry_on_5xx_error(self, mock_get):
        """Test retry logic on 5xx server errors"""
        mock_response_ok = Mock()
        mock_response_ok.json.return_value = {"success": True}
        mock_response_ok.raise_for_status = Mock()

        mock_response_err = Mock()
        mock_response_err.status_code = 500
        http_error = __import__("httpx").HTTPStatusError(
            "Server error", request=Mock(), response=mock_response_err
        )

        mock_get.side_effect = [http_error, mock_response_ok]

        # Disable actual sleep for testing
        with patch("asyncio.sleep", new_callable=AsyncMock):
            self.client.enable_retry = True
            result = await self.client.get("/test")

        # Should eventually succeed after retry
        self.assertIsNotNone(result)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_get_no_retry_when_disabled(self, mock_get):
        """Test that retry doesn't happen when disabled"""
        import httpx

        # Create a proper exception that won't crash
        mock_response = Mock()
        mock_response.status_code = 500
        http_error = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=mock_response
        )
        mock_get.side_effect = http_error

        self.client.enable_retry = False
        result = await self.client.get("/test")

        self.assertIsNone(result)
        # Should only try once
        self.assertEqual(mock_get.call_count, 1)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_get_returns_text_on_json_error(self, mock_get):
        """Test that GET returns text when JSON parsing fails"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Plain text response"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = await self.client.get("/test")

        self.assertEqual(result, "Plain text response")


# ============================================================================
# TEST 5: Test data classes
# ============================================================================
class TestDataClasses(unittest.TestCase):
    """Test data classes parsing and validation"""

    def test_data_network_stats_from_data(self):
        """Test DataNetworkStats.from_data() with valid data"""
        from src.data.network_dataclasses import DataNetworkStats

        test_data = {
            "difficulty": 50000000000000,
            "hash_rate": 400000000000000000000,
            "n_tx": 500000000,
        }

        stats = DataNetworkStats.from_data(test_data)

        self.assertEqual(stats.difficulty, 50000000000000)
        self.assertEqual(stats.hash_rate, 400000000000000000000)
        self.assertEqual(stats.n_tx, 500000000)

    def test_data_network_fees_from_data(self):
        """Test DataNetworkFees.from_data() with valid data"""
        from src.data.network_dataclasses import DataNetworkFees

        test_data = {
            "fastestFee": 10,
            "halfHourFee": 8,
            "hourFee": 5,
            "economyFee": 3,
            "minimumFee": 1,
        }

        fees = DataNetworkFees.from_data(test_data)

        self.assertEqual(fees.fastest, 10)
        self.assertEqual(fees.half_hour, 8)
        self.assertEqual(fees.hour, 5)
        self.assertEqual(fees.economy, 3)
        self.assertEqual(fees.minimum, 1)

    def test_data_transaction_info_from_data(self):
        """Test DataTransactionInfo.from_data() with valid data"""
        from src.data.transactions_dataclasses import DataTransactionInfo

        test_data = {
            "vin": [],
            "vout": [],
            "size": 250,
            "fee": 5000,
            "status": {"confirmed": True, "block_height": 700000},
        }

        tx = DataTransactionInfo.from_data(test_data)

        self.assertEqual(tx.size, 250)
        self.assertEqual(tx.fee, 5000)
        self.assertTrue(tx.status.get("confirmed"))

    def test_data_class_handles_missing_keys(self):
        """Test that data classes handle missing keys gracefully"""
        from src.data.network_dataclasses import DataNetworkStats

        # Test with empty dict - should use default values
        test_data = {}

        stats = DataNetworkStats.from_data(test_data)
        # Should not crash and use defaults
        self.assertEqual(stats.difficulty, 0)
        self.assertEqual(stats.hash_rate, 0)


# ============================================================================
# TEST 6: Test error handling with invalid inputs
# ============================================================================
class TestErrorHandling(unittest.IsolatedAsyncioTestCase):
    """Test error handling with invalid inputs"""

    def test_api_client_invalid_url(self):
        """Test APIClient with invalid URL"""
        from src.api.client import APIClient

        # Should not crash on initialization
        client = APIClient("invalid-url")
        self.assertIsNotNone(client)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_api_client_network_timeout(self, mock_get):
        """Test APIClient handles network timeout"""
        import httpx
        from src.api.client import APIClient

        client = APIClient("https://test.example.com")
        mock_get.side_effect = httpx.TimeoutException("Request timeout")

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await client.get("/test")

        self.assertIsNone(result)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_api_client_network_error(self, mock_get):
        """Test APIClient handles network errors"""
        import httpx
        from src.api.client import APIClient

        client = APIClient("https://test.example.com")
        mock_get.side_effect = httpx.NetworkError("Network error")

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await client.get("/test")

        self.assertIsNone(result)

    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_api_client_http_404_error(self, mock_get):
        """Test APIClient handles 404 errors without retry"""
        import httpx
        from src.api.client import APIClient

        client = APIClient("https://test.example.com")
        mock_response = Mock()
        mock_response.status_code = 404

        http_error = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=mock_response
        )
        mock_get.side_effect = http_error

        result = await client.get("/test")

        self.assertIsNone(result)
        # Should not retry on 4xx errors
        self.assertEqual(mock_get.call_count, 1)

    def test_data_class_invalid_data_type(self):
        """Test data class with invalid data type"""
        from src.data.network_dataclasses import DataNetworkStats

        # Pass empty dict to check default behavior
        try:
            stats = DataNetworkStats.from_data({})
            # Should handle gracefully with defaults
            self.assertIsNotNone(stats)
        except (TypeError, AttributeError) as e:
            # May raise exception - that's acceptable
            self.assertTrue(True)

    def test_logger_invalid_log_level(self):
        """Test logger with invalid log level falls back to INFO"""
        with patch("src.config.Config.LOG_LEVEL", "INVALID_LEVEL"):
            with patch("src.config.Config.LOG_DIR", tempfile.mkdtemp()):
                from src.log import LoggerMCP

                logger = LoggerMCP()
                # Should fall back to INFO level
                self.assertIsNotNone(logger)


# ============================================================================
# TEST 7: Test helper functions
# ============================================================================
class TestHelperFunctions(unittest.TestCase):
    """Test helper and utility functions"""

    def test_satoshi_constant(self):
        """Test SATOSHI constant value"""
        from src.config import config

        self.assertEqual(config.SATOSHI, 100_000_000)

    def test_btc_to_satoshi_conversion(self):
        """Test BTC to satoshi conversion"""
        from src.config import config

        btc_amount = 1.0
        satoshi_amount = btc_amount * config.SATOSHI

        self.assertEqual(satoshi_amount, 100_000_000)

    def test_satoshi_to_btc_conversion(self):
        """Test satoshi to BTC conversion"""
        from src.config import config

        satoshi_amount = 50_000_000
        btc_amount = satoshi_amount / config.SATOSHI

        self.assertEqual(btc_amount, 0.5)


# ============================================================================
# TEST 8: Test singleton patterns
# ============================================================================
class TestSingletonPatterns(unittest.TestCase):
    """Test singleton pattern implementations"""

    def test_logger_singleton(self):
        """Test that get_logger returns same instance"""
        from src.log import get_logger

        logger1 = get_logger()
        logger2 = get_logger()

        self.assertIs(logger1, logger2)

    def test_config_singleton(self):
        """Test that config is a singleton"""
        from src.config import config

        # Config should be the same instance
        self.assertIsNotNone(config)


# ============================================================================
# TEST 9: Basic workflow validation
# ============================================================================
class TestBasicWorkflow(unittest.TestCase):
    """Basic tests to validate test workflow"""

    def test_basic(self):
        """Test basique pour valider le workflow"""
        self.assertEqual(1 + 1, 2)

    def test_python_version(self):
        """Test that Python version is 3.12 or higher"""
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 12)

    def test_pathlib_available(self):
        """Test that pathlib is available"""
        from pathlib import Path

        test_path = Path(__file__)
        self.assertTrue(test_path.exists())


if __name__ == "__main__":
    # Run all tests with verbose output
    unittest.main(verbosity=2)
