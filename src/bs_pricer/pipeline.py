"""End-to-end workflow orchestration."""

from bs_pricer.cleaning import clean_equity_history, clean_option_chain, save_processed_data
from bs_pricer.config import MarketConfig, build_snapshot_id
from bs_pricer.data_download import download_equity_history, download_option_chains, save_raw_data
from bs_pricer.implied_volatility import add_implied_volatility


def run_pipeline(config: MarketConfig | None = None) -> dict[str, object]:
    """Run the full data, pricing, volatility, and plotting workflow."""
    config = config or MarketConfig()
    snapshot_id = build_snapshot_id(config)

    equity_history = download_equity_history(config)
    option_chains = download_option_chains(config)
    equity_raw_path, options_raw_path = save_raw_data(
        equity_history, option_chains, config, snapshot_id
    )

    equity_clean = clean_equity_history(equity_history)
    options_clean = clean_option_chain(option_chains, equity_history, config)
    equity_processed_path, options_processed_path = save_processed_data(
        equity_clean,
        options_clean,
        config,
        snapshot_id,
    )

    options_with_iv = add_implied_volatility(options_clean, config)
    options_with_iv_path = config.processed_data_dir / f"{snapshot_id}_options_with_iv.csv"
    options_with_iv.to_csv(options_with_iv_path, index=False)

    return {
        "config": config,
        "snapshot_id": snapshot_id,
        "equity_history": equity_history,
        "option_chains": option_chains,
        "equity_clean": equity_clean,
        "options_clean": options_clean,
        "options_with_iv": options_with_iv,
        "equity_path": equity_raw_path,
        "options_path": options_raw_path,
        "equity_processed_path": equity_processed_path,
        "options_processed_path": options_processed_path,
        "options_with_iv_path": options_with_iv_path,
    }
