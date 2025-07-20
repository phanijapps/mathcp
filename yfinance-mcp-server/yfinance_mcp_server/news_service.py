"""Simple news service for testing without external dependencies."""

from typing import List
from datetime import datetime, timedelta
from .models import NewsArticle


class NewsService:
    """Service for retrieving news data."""
    
    def get_stock_news(self, symbol: str, limit: int = 10) -> List[NewsArticle]:
        """Get latest news articles for a specific stock."""
        # Mock news data
        mock_news = [
            NewsArticle(
                title=f"{symbol.upper()} Reports Strong Q4 Earnings",
                summary=f"{symbol.upper()} exceeded analyst expectations with strong revenue growth and improved margins.",
                link=f"https://example.com/news/{symbol.lower()}-earnings",
                published=datetime.now() - timedelta(hours=2),
                source="Financial Times",
                sentiment="positive"
            ),
            NewsArticle(
                title=f"{symbol.upper()} Announces New Product Launch",
                summary=f"{symbol.upper()} unveiled its latest innovation, expected to drive future growth.",
                link=f"https://example.com/news/{symbol.lower()}-product",
                published=datetime.now() - timedelta(hours=6),
                source="TechCrunch",
                sentiment="positive"
            ),
            NewsArticle(
                title=f"Analyst Upgrades {symbol.upper()} Price Target",
                summary=f"Wall Street analysts raise price target for {symbol.upper()} citing strong fundamentals.",
                link=f"https://example.com/news/{symbol.lower()}-upgrade",
                published=datetime.now() - timedelta(days=1),
                source="Bloomberg",
                sentiment="positive"
            )
        ]
        
        return mock_news[:limit]
    
    def get_market_news(self, limit: int = 20) -> List[NewsArticle]:
        """Get general market news and analysis."""
        # Mock market news
        mock_news = [
            NewsArticle(
                title="Markets Rally on Strong Economic Data",
                summary="Stock markets surge as latest economic indicators show continued growth momentum.",
                link="https://example.com/news/market-rally",
                published=datetime.now() - timedelta(hours=1),
                source="Reuters",
                sentiment="positive"
            ),
            NewsArticle(
                title="Fed Signals Potential Rate Changes",
                summary="Federal Reserve hints at policy adjustments in upcoming meetings based on inflation data.",
                link="https://example.com/news/fed-signals",
                published=datetime.now() - timedelta(hours=4),
                source="Wall Street Journal",
                sentiment="neutral"
            ),
            NewsArticle(
                title="Tech Sector Shows Resilience",
                summary="Technology stocks continue to outperform despite market volatility concerns.",
                link="https://example.com/news/tech-resilience",
                published=datetime.now() - timedelta(hours=8),
                source="CNBC",
                sentiment="positive"
            ),
            NewsArticle(
                title="Global Markets React to Trade Updates",
                summary="International markets respond to latest developments in trade negotiations.",
                link="https://example.com/news/trade-updates",
                published=datetime.now() - timedelta(days=1),
                source="Financial Times",
                sentiment="neutral"
            )
        ]
        
        return mock_news[:limit]
