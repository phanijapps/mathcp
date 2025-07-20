"""Data models for yfinance MCP server."""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class StockBasicInfo(BaseModel):
    """Basic stock information."""
    symbol: str
    name: str
    sector: str
    industry: str
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_sales: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    book_value: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None
    revenue: Optional[float] = None
    revenue_per_share: Optional[float] = None
    gross_profit: Optional[float] = None
    ebitda: Optional[float] = None
    net_income: Optional[float] = None
    total_cash: Optional[float] = None
    total_debt: Optional[float] = None
    current_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    free_cash_flow: Optional[float] = None
    operating_margin: Optional[float] = None
    profit_margin: Optional[float] = None


class StockPrice(BaseModel):
    """Stock price information."""
    symbol: str
    current_price: float
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    previous_close: float
    change: float
    change_percent: float
    market_cap: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    fifty_day_avg: Optional[float] = None
    two_hundred_day_avg: Optional[float] = None
    timestamp: datetime


class FinancialMetric(BaseModel):
    """Financial metric with value and context."""
    name: str
    value: float
    description: str
    category: str
    unit: Optional[str] = None
    is_positive: bool = True


class FinancialRatios(BaseModel):
    """Key financial ratios for analysis."""
    symbol: str
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_sales: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_investment: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    profit_margin: Optional[float] = None


class NewsArticle(BaseModel):
    """News article information."""
    title: str
    summary: str
    link: str
    published: datetime
    source: str
    sentiment: Optional[str] = None


class TechnicalIndicator(BaseModel):
    """Technical indicator data."""
    name: str
    value: float
    signal: str
    description: str
    period: int


class HistoricalData(BaseModel):
    """Historical stock price data."""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adj_close: float


class OptionsData(BaseModel):
    """Options chain data."""
    symbol: str
    expiration_date: datetime
    calls: List[Dict[str, Any]]
    puts: List[Dict[str, Any]]
    implied_volatility: Optional[float] = None


class ValuationMetrics(BaseModel):
    """Valuation metrics for fundamental analysis."""
    symbol: str
    dcf_value: Optional[float] = None
    graham_number: Optional[float] = None
    buffet_indicator: Optional[float] = None
    fair_value: Optional[float] = None
    margin_of_safety: Optional[float] = None
    upside_potential: Optional[float] = None


class MarketIndicators(BaseModel):
    """Market indicators and signals."""
    symbol: str
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    bollinger_middle: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
