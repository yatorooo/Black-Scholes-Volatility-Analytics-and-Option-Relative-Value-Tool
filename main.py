"""One-button entry point for the Black-Scholes pricer project."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from bs_pricer.config import MarketConfig
from bs_pricer.pipeline import run_pipeline


def main() -> None:
    """Download raw equity and option-chain data."""
    result = run_pipeline(MarketConfig())

    print("Download complete")
    print(f"Equity history: {result['equity_path']}")
    print(f"Option chains: {result['options_path']}")


if __name__ == "__main__":
    main()
