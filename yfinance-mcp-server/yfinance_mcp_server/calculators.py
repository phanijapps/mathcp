"""Financial calculators for stock analysis."""

import numpy as np
from typing import List, Optional, Tuple
from scipy.stats import norm


class FinancialCalculators:
    """Collection of financial calculators for stock analysis."""
    
    @staticmethod
    def calculate_graham_number(eps: float, book_value: float) -> float:
        """Calculate Graham number for fair value estimation."""
        if eps <= 0 or book_value <= 0:
            return 0.0
        return np.sqrt(22.5 * eps * book_value)
    
    @staticmethod
    def calculate_dcf_value(free_cash_flow: float, growth_rate: float = 0.03, discount_rate: float = 0.10) -> float:
        """Calculate DCF value using simplified model."""
        if free_cash_flow <= 0:
            return 0.0
        return free_cash_flow * (1 + growth_rate) / (discount_rate - growth_rate)
    
    @staticmethod
    def calculate_pe_ratio(price: float, eps: float) -> float:
        """Calculate P/E ratio."""
        if eps <= 0:
            return 0.0
        return price / eps
    
    @staticmethod
    def calculate_roe(net_income: float, shareholders_equity: float) -> float:
        """Calculate Return on Equity."""
        if shareholders_equity <= 0:
            return 0.0
        return (net_income / shareholders_equity) * 100
    
    @staticmethod
    def calculate_roa(net_income: float, total_assets: float) -> float:
        """Calculate Return on Assets."""
        if total_assets <= 0:
            return 0.0
        return (net_income / total_assets) * 100
    
    @staticmethod
    def calculate_debt_to_equity(total_debt: float, shareholders_equity: float) -> float:
        """Calculate Debt to Equity ratio."""
        if shareholders_equity <= 0:
            return 0.0
        return total_debt / shareholders_equity
    
    @staticmethod
    def calculate_current_ratio(current_assets: float, current_liabilities: float) -> float:
        """Calculate Current Ratio."""
        if current_liabilities <= 0:
            return 0.0
        return current_assets / current_liabilities
    
    @staticmethod
    def calculate_quick_ratio(current_assets: float, inventory: float, current_liabilities: float) -> float:
        """Calculate Quick Ratio."""
        if current_liabilities <= 0:
            return 0.0
        return (current_assets - inventory) / current_liabilities
    
    @staticmethod
    def calculate_net_margin(net_income: float, revenue: float) -> float:
        """Calculate Net Profit Margin."""
        if revenue <= 0:
            return 0.0
        return (net_income / revenue) * 100
    
    @staticmethod
    def calculate_black_scholes_call(
        stock_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """Calculate Black-Scholes call option price."""
        if time_to_expiry <= 0 or volatility <= 0:
            return 0.0
        
        d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
        d2 = d1 - volatility * np.sqrt(time_to_expiry)
        
        call_price = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
        return max(0, call_price)
    
    @staticmethod
    def calculate_black_scholes_put(
        stock_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """Calculate Black-Scholes put option price."""
        if time_to_expiry <= 0 or volatility <= 0:
            return 0.0
        
        d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
        d2 = d1 - volatility * np.sqrt(time_to_expiry)
        
        put_price = strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
        return max(0, put_price)
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        if not returns:
            return 0.0
        
        returns_array = np.array(returns)
        excess_returns = returns_array - risk_free_rate / 252  # Daily risk-free rate
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0.0
    
    @staticmethod
    def calculate_maximum_drawdown(prices: List[float]) -> float:
        """Calculate maximum drawdown."""
        if not prices:
            return 0.0
        
        prices_array = np.array(prices)
        peak = np.maximum.accumulate(prices_array)
        drawdown = (prices_array - peak) / peak
        return np.min(drawdown) * 100
    
    @staticmethod
    def calculate_value_at_risk(returns: List[float], confidence_level: float = 0.05) -> float:
        """Calculate Value at Risk (VaR)."""
        if not returns:
            return 0.0
        
        returns_array = np.array(returns)
        return np.percentile(returns_array, confidence_level * 100)
    
    @staticmethod
    def calculate_beta(stock_returns: List[float], market_returns: List[float]) -> float:
        """Calculate beta coefficient."""
        if len(stock_returns) != len(market_returns) or len(stock_returns) < 2:
            return 0.0
        
        stock_array = np.array(stock_returns)
        market_array = np.array(market_returns)
        
        covariance = np.cov(stock_array, market_array)[0, 1]
        market_variance = np.var(market_array)
        
        return covariance / market_variance if market_variance > 0 else 0.0
