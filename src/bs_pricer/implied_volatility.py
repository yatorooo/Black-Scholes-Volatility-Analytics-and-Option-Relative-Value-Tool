"""Solve implied volatility from observed option prices."""

import pandas as pd
from scipy.optimize import brentq

from bs_pricer.black_scholes import price_option
from bs_pricer.config import MarketConfig


def implied_volatility(
    market_price: float,
    option_type: str,
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    dividend_yield: float = 0.0,
    lower_bound: float = 1e-4,
    upper_bound: float = 5.0,
) -> float:
    """Solve one option's implied volatility."""

    def pricing_error(volatility: float) -> float:
        return (
            price_option(
                option_type=option_type,
                spot=spot,
                strike=strike,
                time_to_expiry=time_to_expiry,
                rate=rate,
                volatility=volatility,
                dividend_yield=dividend_yield,
            )
            - market_price
        )

    return brentq(pricing_error, lower_bound, upper_bound)


def _solve_row_iv(row: pd.Series, config: MarketConfig) -> float:
    if row.time_to_expiry <= 0 or row.mid_price <= 0:
        return float("nan")

    try:
        return implied_volatility(
            market_price=row.mid_price,
            option_type=row.option_type,
            spot=row.spot,
            strike=row.strike,
            time_to_expiry=row.time_to_expiry,
            rate=config.risk_free_rate,
            dividend_yield=config.dividend_yield,
        )
    except (ValueError, ZeroDivisionError):
        return float("nan")


def add_implied_volatility(options: pd.DataFrame, config: MarketConfig) -> pd.DataFrame:
    """Apply implied-volatility solving to an option-chain dataset."""
    options_with_iv = options.copy()
    options_with_iv["solved_iv"] = [
        _solve_row_iv(row, config) for row in options_with_iv.itertuples(index=False)
    ]

    return options_with_iv
