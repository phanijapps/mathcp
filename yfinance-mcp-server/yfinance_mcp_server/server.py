"""Main FastMCP server implementation for yfinance."""

from fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from .stock_data_simple import StockDataService
from .news_service import NewsService
from .calculators import FinancialCalculators
from .config import get_config

# Initialize services
stock_service = StockDataService()
news_service = NewsService()
calculator_service = FinancialCalculators()
config = get_config()

# Create FastMCP server
mcp = FastMCP("yfinance-mcp-server")


@mcp.tool()
async def get_stock_basic_info(symbol: str) -> Dict[str, Any]:
    """Get basic stock information including company details and key metrics."""
    info = stock_service.get_basic_info(symbol)
    return info.dict()


@mcp.tool()
async def get_current_price(symbol: str) -> Dict[str, Any]:
    """Get current stock price and trading information."""
    price = stock_service.get_current_price(symbol)
    return price.dict()


@mcp.tool()
async def get_financial_ratios(symbol: str) -> Dict[str, Any]:
    """Get comprehensive financial ratios for stock analysis."""
    ratios = stock_service.get_financial_ratios(symbol)
    return ratios.dict()


@mcp.tool()
async def get_historical_data(symbol: str, period: str = "1y") -> List[Dict[str, Any]]:
    """Get historical stock price data."""
    data = stock_service.get_historical_data(symbol, period)
    return [d.dict() for d in data]


@mcp.tool()
async def get_technical_indicators(symbol: str, period: str = "1y") -> Dict[str, Any]:
    """Get technical indicators including RSI, MACD, Bollinger Bands, etc."""
    indicators = stock_service.get_technical_indicators(symbol, period)
    return indicators.dict()


@mcp.tool()
async def get_valuation_metrics(symbol: str) -> Dict[str, Any]:
    """Get valuation metrics using Graham, DCF, and Buffet models."""
    metrics = stock_service.get_valuation_metrics(symbol)
    return metrics.dict()


@mcp.tool()
async def get_options_data(symbol: str) -> Dict[str, Any]:
    """Get options chain data including calls, puts, and Greeks."""
    options = stock_service.get_options_data(symbol)
    return options


@mcp.tool()
async def get_stock_news(symbol: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get latest news articles for a specific stock."""
    news = news_service.get_stock_news(symbol, limit)
    return [n.dict() for n in news]


@mcp.tool()
async def get_market_news(limit: int = 20) -> List[Dict[str, Any]]:
    """Get general market news and analysis."""
    news = news_service.get_market_news(limit)
    return [n.dict() for n in news]


@mcp.tool()
async def calculate_black_scholes(
    stock_price: float,
    strike_price: float,
    time_to_expiry: float,
    volatility: float,
    risk_free_rate: float = 0.05,
    option_type: str = "call"
) -> Dict[str, float]:
    """Calculate Black-Scholes option pricing."""
    if option_type.lower() == "call":
        price = calculator_service.calculate_black_scholes_call(
            stock_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
    else:
        price = calculator_service.calculate_black_scholes_put(
            stock_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
    
    return {"option_price": price, "option_type": option_type}


@mcp.tool()
async def calculate_financial_ratios(
    net_income: Optional[float] = None,
    revenue: Optional[float] = None,
    total_assets: Optional[float] = None,
    shareholders_equity: Optional[float] = None,
    total_debt: Optional[float] = None,
    current_assets: Optional[float] = None,
    current_liabilities: Optional[float] = None,
    inventory: Optional[float] = None
) -> Dict[str, float]:
    """Calculate custom financial ratios and metrics."""
    results = {}
    
    if net_income is not None and total_assets is not None:
        results["return_on_assets"] = calculator_service.calculate_roa(net_income, total_assets)
    
    if net_income is not None and shareholders_equity is not None:
        results["return_on_equity"] = calculator_service.calculate_roe(net_income, shareholders_equity)
    
    if net_income is not None and revenue is not None:
        results["net_margin"] = calculator_service.calculate_net_margin(net_income, revenue)
    
    if total_debt is not None and shareholders_equity is not None:
        results["debt_to_equity"] = calculator_service.calculate_debt_to_equity(total_debt, shareholders_equity)
    
    if current_assets is not None and current_liabilities is not None:
        results["current_ratio"] = calculator_service.calculate_current_ratio(current_assets, current_liabilities)
    
    if current_assets is not None and inventory is not None and current_liabilities is not None:
        results["quick_ratio"] = calculator_service.calculate_quick_ratio(current_assets, inventory, current_liabilities)
    
    return results


if __name__ == "__main__":
    mcp.run()
