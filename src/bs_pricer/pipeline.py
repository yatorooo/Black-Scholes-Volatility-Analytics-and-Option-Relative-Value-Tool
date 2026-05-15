"""End-to-end workflow orchestration."""

from bs_pricer.cleaning import clean_equity_history, clean_option_chain, save_processed_data
from bs_pricer.config import MarketConfig
from bs_pricer.data_download import download_equity_history, download_option_chains, save_raw_data


def run_pipeline(config: MarketConfig | None = None) -> dict[str, object]:
    """Run the full data, pricing, volatility, and plotting workflow."""
    config = config or MarketConfig()

    equity_history = download_equity_history(config)
    option_chains = download_option_chains(config)
    equity_raw_path, options_raw_path = save_raw_data(equity_history, option_chains, config)

    equity_clean = clean_equity_history(equity_history)
    options_clean = clean_option_chain(option_chains, equity_history, config)
    equity_processed_path, options_processed_path = save_processed_data(
        equity_clean,
        options_clean,
        config,
    )

    return {
        "config": config,
        "equity_history": equity_history,
        "option_chains": option_chains,
        "equity_clean": equity_clean,
        "options_clean": options_clean,
        "equity_path": equity_raw_path,
        "options_path": options_raw_path,
        "equity_processed_path": equity_processed_path,
        "options_processed_path": options_processed_path,
    }
