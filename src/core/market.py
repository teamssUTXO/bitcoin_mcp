from typing import Dict, Optional
from src.api.coingecko_client import CoinGeckoClient


class MarketAnalyzer:
    def __init__(self):
        self.coingecko = CoinGeckoClient()
    
    def get_market_sentiment(self) -> Dict:
        """Analyse complète du sentiment de marché"""
        price_data = self.coingecko.get_bitcoin_price_detailed()
        fng = self.coingecko.get_fear_and_greed()
        global_data = self.coingecko.get_global_data()
        
        if not price_data:
            return {"error": "Price data unavailable"}
        
        price = price_data.get('usd', 0)
        change_24h = price_data.get('usd_24h_change', 0)
        volume_24h = price_data.get('usd_24h_vol', 0)
        market_cap = price_data.get('usd_market_cap', 0)
        
        # Tendance
        trend = "BULLISH" if change_24h > 2 else "BEARISH" if change_24h < -2 else "NEUTRAL"
        
        # Sentiment
        fng_value = int(fng.get('value', 50)) if fng else 50
        sentiment = fng.get('value_classification', 'Neutral') if fng else 'Unknown'
        
        # Interprétation
        interpretation = self._interpret_fng(fng_value)
        
        # Dominance
        btc_dominance = 0
        total_market_cap = 0
        dominance_signal = "BALANCED"
        
        if global_data:
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
            total_market_cap = global_data.get('total_market_cap', {}).get('usd', 0)
            dominance_signal = "BTC SEASON" if btc_dominance > 55 else "ALTCOIN SEASON" if btc_dominance < 45 else "BALANCED"
        
        # Signaux de trading
        signals = self._generate_trading_signals(
            change_24h, fng_value, volume_24h, market_cap
        )
        
        return {
            "price_usd": price,
            "change_24h_percent": change_24h,
            "volume_24h_usd": volume_24h,
            "market_cap_usd": market_cap,
            "trend": trend,
            "fear_greed_index": fng_value,
            "sentiment": sentiment,
            "sentiment_interpretation": interpretation,
            "btc_dominance_percent": btc_dominance,
            "total_crypto_market_cap_usd": total_market_cap,
            "market_phase": dominance_signal,
            "trading_signals": signals
        }
    
    def _interpret_fng(self, value: int) -> str:
        """Interprète le Fear & Greed Index"""
        if value >= 75:
            return "Extreme Greed - Consider taking profits"
        elif value >= 55:
            return "Greed - Bullish sentiment dominates"
        elif value >= 45:
            return "Neutral - Market indecision"
        elif value >= 25:
            return "Fear - Bearish sentiment present"
        else:
            return "Extreme Fear - Potential buying opportunity"
    
    def _generate_trading_signals(
        self, change_24h: float, fng: int, volume: float, mcap: float
    ) -> list:
        """Génère des signaux de trading basés sur les métriques"""
        signals = []
        
        if change_24h > 5:
            signals.append(f"Strong upward momentum (+{change_24h:.1f}%)")
        elif change_24h < -5:
            signals.append(f"Strong downward pressure ({change_24h:.1f}%)")
        else:
            signals.append(f"Consolidation phase ({change_24h:+.1f}%)")
        
        if fng > 75 and change_24h > 3:
            signals.append("Overheated - Risk of correction")
        elif fng < 25 and change_24h < -3:
            signals.append("Oversold - Potential reversal zone")
        
        if mcap > 0:
            volume_ratio = (volume / mcap) * 100
            if volume_ratio > 5:
                signals.append(f"High trading activity ({volume_ratio:.1f}% of market cap)")
            else:
                signals.append(f"Low trading activity ({volume_ratio:.1f}% of market cap)")
        
        return signals