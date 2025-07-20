"""Stock data service for retrieving and processing financial data."""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import ta
from .models import (
    StockInfo, CurrentPrice, FinancialRatios, 
    HistoricalData, TechnicalIndicators, ValuationMetrics
)
from .calculators import FinancialCalculators


class StockDataService:
    """Service for retrieving and processing stock data."""
    
    def __init__(self):
        self.calculator = FinancialCalculators()
    
    def get_basic_info(self, symbol: str) -> StockInfo:
        """Get basic stock information."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return StockInfo(
                symbol=symbol.upper(),
                name=info.get('longName', 'N/A'),
                sector=info.get('sector', 'N/A'),
                industry=info.get('industry', 'N/A'),
                market_cap=info.get('marketCap', 0),
                enterprise_value=info.get('enterpriseValue', 0),
                pe_ratio=info.get('trailingPE', 0),
                forward_pe=info.get('forwardPE', 0),
                peg_ratio=info.get('pegRatio', 0),
                price_to_book=info.get('priceToBook', 0),
                price_to_sales=info.get('priceToSalesTrailing12Months', 0),
                dividend_yield=info.get('dividendYield', 0),
                beta=info.get('beta', 0),
                fifty_two_week_high=info.get('fiftyTwoWeekHigh', 0),
                fifty_two_week_low=info.get('fiftyTwoWeekLow', 0),
                avg_volume=info.get('averageVolume', 0),
                shares_outstanding=info.get('sharesOutstanding', 0)
            )
        except Exception as e:
            # Return default values if data unavailable
            return StockInfo(
                symbol=symbol.upper(),
                name=f"Data unavailable for {symbol}",
                sector="N/A",
                industry="N/A"
            )
    
    def get_current_price(self, symbol: str) -> CurrentPrice:
        """Get current stock price information."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            info = ticker.info
            
            if not hist.empty:
                latest = hist.iloc[-1]
                return CurrentPrice(
                    symbol=symbol.upper(),
                    current_price=float(latest['Close']),
                    open_price=float(latest['Open']),
                    high_price=float(latest['High']),
                    low_price=float(latest['Low']),
                    volume=int(latest['Volume']),
                    previous_close=info.get('previousClose', float(latest['Close'])),
                    change=float(latest['Close']) - info.get('previousClose', float(latest['Close'])),
                    change_percent=((float(latest['Close']) - info.get('previousClose', float(latest['Close']))) / info.get('previousClose', float(latest['Close']))) * 100 if info.get('previousClose') else 0,
                    timestamp=datetime.now()
                )
        except Exception:
            pass
        
        # Return default if error
        return CurrentPrice(
            symbol=symbol.upper(),
            current_price=0.0,
            timestamp=datetime.now()
        )
    
    def get_financial_ratios(self, symbol: str) -> FinancialRatios:
        """Get comprehensive financial ratios."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            
            # Extract financial data
            net_income = 0
            revenue = 0
            total_assets = 0
            shareholders_equity = 0
            total_debt = 0
            current_assets = 0
            current_liabilities = 0
            
            if not financials.empty:
                latest_financials = financials.iloc[:, 0]
                net_income = latest_financials.get('Net Income', 0)
                revenue = latest_financials.get('Total Revenue', 0)
            
            if not balance_sheet.empty:
                latest_balance = balance_sheet.iloc[:, 0]
                total_assets = latest_balance.get('Total Assets', 0)
                shareholders_equity = latest_balance.get('Stockholders Equity', 0)
                total_debt = latest_balance.get('Total Debt', 0)
                current_assets = latest_balance.get('Current Assets', 0)
                current_liabilities = latest_balance.get('Current Liabilities', 0)
            
            return FinancialRatios(
                symbol=symbol.upper(),
                pe_ratio=info.get('trailingPE', 0),
                forward_pe=info.get('forwardPE', 0),
                peg_ratio=info.get('pegRatio', 0),
                price_to_book=info.get('priceToBook', 0),
                price_to_sales=info.get('priceToSalesTrailing12Months', 0),
                return_on_equity=self.calculator.calculate_roe(net_income, shareholders_equity),
                return_on_assets=self.calculator.calculate_roa(net_income, total_assets),
                debt_to_equity=self.calculator.calculate_debt_to_equity(total_debt, shareholders_equity),
                current_ratio=self.calculator.calculate_current_ratio(current_assets, current_liabilities),
                quick_ratio=self.calculator.calculate_quick_ratio(current_assets, 0, current_liabilities),
                gross_margin=info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
                operating_margin=info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                net_margin=self.calculator.calculate_net_margin(net_income, revenue),
                asset_turnover=revenue / total_assets if total_assets > 0 else 0,
                inventory_turnover=0,  # Would need cost of goods sold
                receivables_turnover=0  # Would need accounts receivable
            )
        except Exception:
            return FinancialRatios(symbol=symbol.upper())
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> List[HistoricalData]:
        """Get historical stock price data."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            data = []
            for date, row in hist.iterrows():
                data.append(HistoricalData(
                    symbol=symbol.upper(),
                    date=date.date(),
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    volume=int(row['Volume']),
                    adjusted_close=float(row['Close'])
                ))
            
            return data
        except Exception:
            return []
    
    def get_technical_indicators(self, symbol: str, period: str = "1y") -> TechnicalIndicators:
        """Get technical indicators for stock analysis."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return TechnicalIndicators(symbol=symbol.upper())
            
            # Calculate indicators
            rsi = ta.momentum.RSIIndicator(hist['Close']).rsi().iloc[-1]
            
            # MACD
            macd_indicator = ta.trend.MACD(hist['Close'])
            macd = macd_indicator.macd().iloc[-1]
            macd_signal = macd_indicator.macd_signal().iloc[-1]
            macd_histogram = macd_indicator.macd_diff().iloc[-1]
            
            # Bollinger Bands
            bb_indicator = ta.volatility.BollingerBands(hist['Close'])
            bb_upper = bb_indicator.bollinger_hband().iloc[-1]
            bb_lower = bb_indicator.bollinger_lband().iloc[-1]
            bb_middle = bb_indicator.bollinger_mavg().iloc[-1]
            
            # Moving averages
            sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            ema_12 = hist['Close'].ewm(span=12).mean().iloc[-1]
            ema_26 = hist['Close'].ewm(span=26).mean().iloc[-1]
            
            # Volume indicators
            volume_sma = hist['Volume'].rolling(window=20).mean().iloc[-1]
            
            return TechnicalIndicators(
                symbol=symbol.upper(),
                rsi=float(rsi) if not pd.isna(rsi) else 0,
                macd=float(macd) if not pd.isna(macd) else 0,
                macd_signal=float(macd_signal) if not pd.isna(macd_signal) else 0,
                macd_histogram=float(macd_histogram) if not pd.isna(macd_histogram) else 0,
                bollinger_upper=float(bb_upper) if not pd.isna(bb_upper) else 0,
                bollinger_lower=float(bb_lower) if not pd.isna(bb_lower) else 0,
                bollinger_middle=float(bb_middle) if not pd.isna(bb_middle) else 0,
                sma_20=float(sma_20) if not pd.isna(sma_20) else 0,
                sma_50=float(sma_50) if not pd.isna(sma_50) else 0,
                ema_12=float(ema_12) if not pd.isna(ema_12) else 0,
                ema_26=float(ema_26) if not pd.isna(ema_26) else 0,
                volume_sma=float(volume_sma) if not pd.isna(volume_sma) else 0
            )
        except Exception:
            return TechnicalIndicators(symbol=symbol.upper())
    
    def get_valuation_metrics(self, symbol: str) -> ValuationMetrics:
        """Get valuation metrics using various models."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get financial data for calculations
            eps = info.get('trailingEps', 0)
            book_value = info.get('bookValue', 0)
            free_cash_flow = info.get('freeCashflow', 0)
            current_price = info.get('currentPrice', 0)
            
            # Calculate valuation metrics
            graham_number = self.calculator.calculate_graham_number(eps, book_value)
            dcf_value = self.calculator.calculate_dcf_value(free_cash_flow) if free_cash_flow > 0 else 0
            
            return ValuationMetrics(
                symbol=symbol.upper(),
                graham_number=graham_number,
                dcf_value=dcf_value,
                current_price=current_price,
                fair_value_estimate=(graham_number + dcf_value) / 2 if graham_number > 0 and dcf_value > 0 else 0,
                upside_potential=((graham_number - current_price) / current_price * 100) if current_price > 0 and graham_number > 0 else 0,
                margin_of_safety=((graham_number - current_price) / graham_number * 100) if graham_number > 0 else 0
            )
        except Exception:
            return ValuationMetrics(symbol=symbol.upper())
    
    def get_options_data(self, symbol: str) -> Dict[str, Any]:
        """Get options chain data."""
        try:
            ticker = yf.Ticker(symbol)
            options_dates = ticker.options
            
            if not options_dates:
                return {"error": "No options data available"}
            
            # Get options for the nearest expiration
            nearest_expiry = options_dates[0]
            options_chain = ticker.option_chain(nearest_expiry)
            
            calls = options_chain.calls.to_dict('records')
            puts = options_chain.puts.to_dict('records')
            
            return {
                "symbol": symbol.upper(),
                "expiration_date": nearest_expiry,
                "calls": calls[:10],  # Limit to first 10
                "puts": puts[:10]     # Limit to first 10
            }
        except Exception as e:
            return {"error": f"Unable to retrieve options data: {str(e)}"}
