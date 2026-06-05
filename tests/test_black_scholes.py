"""Tests for Black-Scholes pricing."""

from pytest import approx

from bs_pricer.black_scholes import price_call, price_option, price_put


def test_price_call_known_value():
    price = price_call(spot=100, strike=100, time_to_expiry=1, rate=0.05, volatility=0.2)

    assert price == approx(10.4506, abs=1e-4)


def test_price_put_known_value():
    price = price_put(spot=100, strike=100, time_to_expiry=1, rate=0.05, volatility=0.2)

    assert price == approx(5.5735, abs=1e-4)


def test_price_option_dispatches_by_type():
    call = price_option("call", spot=100, strike=100, time_to_expiry=1, rate=0.05, volatility=0.2)
    put = price_option("put", spot=100, strike=100, time_to_expiry=1, rate=0.05, volatility=0.2)

    assert call == approx(10.4506, abs=1e-4)
    assert put == approx(5.5735, abs=1e-4)
