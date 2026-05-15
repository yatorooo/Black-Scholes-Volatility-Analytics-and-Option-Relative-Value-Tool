"""Project configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarketConfig:
    """Inputs shared across the pricing and volatility workflow."""

    ticker: str = "AAPL"
    start_date: str = "2020-01-01"
    end_date: str | None = None
    risk_free_rate: float = 0.05
    dividend_yield: float = 0.0
    trading_days_per_year: int = 252
    raw_data_dir: Path = Path("data/raw")
    processed_data_dir: Path = Path("data/processed")
