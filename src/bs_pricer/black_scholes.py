"""Black-Scholes pricing functions."""

from math import exp, log, sqrt

from scipy.stats import norm


def _d1(spot: float, strike: float, time_to_expiry: float, rate: float, volatility: float, dividend_yield: float) -> float:
    return (
        log(spot / strike)
        + (rate - dividend_yield + 0.5 * volatility**2) * time_to_expiry
    ) / (volatility * sqrt(time_to_expiry))


def _d2(d1: float, volatility: float, time_to_expiry: float) -> float:
    return d1 - volatility * sqrt(time_to_expiry)


def price_call(
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    """Price a European call option."""
    d1 = _d1(spot, strike, time_to_expiry, rate, volatility, dividend_yield)
    d2 = _d2(d1, volatility, time_to_expiry)

    return spot * exp(-dividend_yield * time_to_expiry) * norm.cdf(d1) - strike * exp(
        -rate * time_to_expiry
    ) * norm.cdf(d2)


def price_put(
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    """Price a European put option."""
    d1 = _d1(spot, strike, time_to_expiry, rate, volatility, dividend_yield)
    d2 = _d2(d1, volatility, time_to_expiry)

    return strike * exp(-rate * time_to_expiry) * norm.cdf(-d2) - spot * exp(
        -dividend_yield * time_to_expiry
    ) * norm.cdf(-d1)


def price_option(
    option_type: str,
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    """Price a European call or put option using Black-Scholes."""
    if option_type == "call":
        return price_call(spot, strike, time_to_expiry, rate, volatility, dividend_yield)
    if option_type == "put":
        return price_put(spot, strike, time_to_expiry, rate, volatility, dividend_yield)

    raise ValueError("option_type must be 'call' or 'put'")
