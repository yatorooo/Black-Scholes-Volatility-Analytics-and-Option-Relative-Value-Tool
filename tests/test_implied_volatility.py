"""Tests for implied-volatility solving."""

import pandas as pd
from pytest import approx

from bs_pricer.black_scholes import price_call, price_put
from bs_pricer.config import MarketConfig
from bs_pricer.implied_volatility import add_implied_volatility, implied_volatility


def test_implied_volatility_recovers_call_volatility():
    market_price = price_call(
        spot=100,
        strike=100,
        time_to_expiry=1,
        rate=0.05,
        volatility=0.2,
    )

    solved_iv = implied_volatility(
        market_price=market_price,
        option_type="call",
        spot=100,
        strike=100,
        time_to_expiry=1,
        rate=0.05,
    )

    assert solved_iv == approx(0.2, abs=1e-6)


def test_implied_volatility_recovers_put_volatility():
    market_price = price_put(
        spot=100,
        strike=100,
        time_to_expiry=1,
        rate=0.05,
        volatility=0.2,
    )

    solved_iv = implied_volatility(
        market_price=market_price,
        option_type="put",
        spot=100,
        strike=100,
        time_to_expiry=1,
        rate=0.05,
    )

    assert solved_iv == approx(0.2, abs=1e-6)


def test_add_implied_volatility_adds_solved_iv_column():
    config = MarketConfig(risk_free_rate=0.05, dividend_yield=0.0)
    call_price = price_call(100, 100, 1, 0.05, 0.2)
    put_price = price_put(100, 100, 1, 0.05, 0.25)
    options = pd.DataFrame(
        {
            "option_type": ["call", "put"],
            "mid_price": [call_price, put_price],
            "spot": [100, 100],
            "strike": [100, 100],
            "time_to_expiry": [1, 1],
        }
    )

    result = add_implied_volatility(options, config)

    assert result["solved_iv"].tolist() == approx([0.2, 0.25], abs=1e-6)


def test_add_implied_volatility_keeps_unsolved_rows_as_nan():
    config = MarketConfig(risk_free_rate=0.05, dividend_yield=0.0)
    options = pd.DataFrame(
        {
            "option_type": ["call"],
            "mid_price": [10_000.0],
            "spot": [100.0],
            "strike": [100.0],
            "time_to_expiry": [1.0],
        }
    )

    result = add_implied_volatility(options, config)

    assert pd.isna(result.loc[0, "solved_iv"])


def test_add_implied_volatility_keeps_zero_maturity_rows_as_nan():
    config = MarketConfig(risk_free_rate=0.05, dividend_yield=0.0)
    options = pd.DataFrame(
        {
            "option_type": ["call"],
            "mid_price": [1.0],
            "spot": [100.0],
            "strike": [100.0],
            "time_to_expiry": [0.0],
        }
    )

    result = add_implied_volatility(options, config)

    assert pd.isna(result.loc[0, "solved_iv"])
