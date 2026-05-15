"""Clean and normalize equity and option market data."""

from pathlib import Path

import numpy as np
import pandas as pd

from bs_pricer.config import MarketConfig


def clean_equity_history(equity_history: pd.DataFrame) -> pd.DataFrame:
    """Clean historical equity price data and add log returns."""
    equity = equity_history.copy()

    equity.index = pd.to_datetime(equity.index).tz_localize(None)
    equity = equity.rename_axis("date").reset_index()
    equity.columns = equity.columns.str.lower().str.replace(" ", "_")

    price_col = "adj_close" if "adj_close" in equity.columns else "close"
    equity["log_return"] = np.log(equity[price_col] / equity[price_col].shift(1))

    return equity


def add_option_features(
    option_chains: pd.DataFrame,
    spot_price: float,
    config: MarketConfig,
) -> pd.DataFrame:
    """Add mid price, moneyness, and time-to-expiry fields."""
    options = option_chains.copy()

    options["expiry"] = pd.to_datetime(options["expiry"])
    valuation_date = pd.Timestamp.today().normalize()

    options["mid_price"] = (options["bid"] + options["ask"]) / 2
    options["spot"] = spot_price
    options["moneyness"] = options["strike"] / options["spot"]
    options["days_to_expiry"] = (options["expiry"] - valuation_date).dt.days
    options["time_to_expiry"] = options["days_to_expiry"] / config.trading_days_per_year

    return options


def clean_option_chain(
    option_chains: pd.DataFrame,
    equity_history: pd.DataFrame,
    config: MarketConfig,
) -> pd.DataFrame:
    """Clean option-chain data and add pricing features."""
    equity = clean_equity_history(equity_history)
    price_col = "adj_close" if "adj_close" in equity.columns else "close"
    spot_price = float(equity[price_col].dropna().iloc[-1])

    options = add_option_features(option_chains, spot_price, config)
    options.columns = options.columns.str.lower().str.replace(" ", "_")

    columns = [
        "contractsymbol",
        "option_type",
        "expiry",
        "strike",
        "lastprice",
        "bid",
        "ask",
        "mid_price",
        "volume",
        "openinterest",
        "impliedvolatility",
        "spot",
        "moneyness",
        "days_to_expiry",
        "time_to_expiry",
    ]

    return options[columns]


def save_processed_data(
    equity_clean: pd.DataFrame,
    options_clean: pd.DataFrame,
    config: MarketConfig,
) -> tuple[Path, Path]:
    """Persist cleaned datasets."""
    config.processed_data_dir.mkdir(parents=True, exist_ok=True)

    equity_path = config.processed_data_dir / f"{config.ticker}_equity_clean.csv"
    options_path = config.processed_data_dir / f"{config.ticker}_options_clean.csv"

    equity_clean.to_csv(equity_path, index=False)
    options_clean.to_csv(options_path, index=False)

    return equity_path, options_path
