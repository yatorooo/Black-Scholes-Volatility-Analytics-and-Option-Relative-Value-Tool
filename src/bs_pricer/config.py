"""Project configuration."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class MarketConfig:
    """Inputs shared across the pricing and volatility workflow."""

    ticker: str = "AAPL"
    tag: str = ""
    start_date: str = "2020-01-01"
    end_date: str | None = None
    risk_free_rate: float = 0.05
    dividend_yield: float = 0.0
    trading_days_per_year: int = 252
    raw_data_dir: Path = Path("data/raw")
    processed_data_dir: Path = Path("data/processed")


def build_snapshot_id(config: MarketConfig, timestamp: datetime | None = None) -> str:
    """Build a unique, sortable id for one downloaded market snapshot."""
    parts = [config.ticker]
    if config.tag:
        parts.append(config.tag)
    parts.append((timestamp or datetime.now()).strftime("%Y%m%dT%H%M%S"))
    return "_".join(parts)


def list_snapshots(config: MarketConfig) -> list[str]:
    """List previously saved snapshot ids for this ticker, most recent first."""
    suffix = "_options_with_iv.csv"
    files = config.processed_data_dir.glob(f"{config.ticker}_*{suffix}")
    files = sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)
    return [f.name[: -len(suffix)] for f in files]
