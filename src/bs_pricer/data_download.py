"""Download historical equity data and option chains from yfinance."""

from pathlib import Path

import pandas as pd
import yfinance as yf

from bs_pricer.config import MarketConfig


def download_equity_history(config: MarketConfig) -> pd.DataFrame:
    """Download historical equity prices."""
    ticker = yf.Ticker(config.ticker)
    return ticker.history(start=config.start_date, end=config.end_date, auto_adjust=False)


def download_option_chains(config: MarketConfig) -> pd.DataFrame:
    """Download option-chain data for available expiries."""
    ticker = yf.Ticker(config.ticker)
    option_frames = []

    for expiry in ticker.options:
        chain = ticker.option_chain(expiry)
        calls = chain.calls.assign(expiry=expiry, option_type="call")
        puts = chain.puts.assign(expiry=expiry, option_type="put")
        option_frames.extend([calls, puts])

    return pd.concat(option_frames, ignore_index=True)


def save_raw_data(
    equity_history: pd.DataFrame,
    option_chains: pd.DataFrame,
    config: MarketConfig,
    snapshot_id: str,
) -> tuple[Path, Path]:
    """Persist raw downloaded datasets."""
    config.raw_data_dir.mkdir(parents=True, exist_ok=True)

    equity_path = config.raw_data_dir / f"{snapshot_id}_equity_history.csv"
    options_path = config.raw_data_dir / f"{snapshot_id}_option_chains.csv"

    equity_history.to_csv(equity_path)
    option_chains.to_csv(options_path, index=False)

    return equity_path, options_path
