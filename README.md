# Black-Scholes Volatility Analytics and Option Relative Value Tool

This project is structured to build a Python workflow for pricing listed equity options with the Black-Scholes model, estimating implied volatility from market option prices, comparing it with realized historical volatility, and visualizing the volatility smile and volatility surface.

## Project Objectives

1. Download market data from Yahoo Finance through `yfinance`.
2. Clean and normalize equity and option-chain data.
3. Price European call and put options using the Black-Scholes model.
4. Solve implied volatility from observed option market prices.
5. Estimate realised historical volatility from equity returns.
6. Compare implied volatility against historical volatility.
7. Plot volatility smiles by expiry.
8. Plot a volatility surface across strike and maturity.

## Proposed Workflow

1. **Configuration**
   - Select ticker, date range, risk-free rate source or assumption, dividend yield assumption, and target option expiries.

2. **Data Download**
   - Download historical equity prices.
   - Download available option chains by expiry.
   - Save raw snapshots under `data/raw/`.

3. **Data Cleaning**
   - Standardize column names and types.
   - Remove stale, missing, crossed, or illiquid option quotes.
   - Compute mid prices from bid and ask quotes.
   - Add time-to-expiry and moneyness fields.
   - Save cleaned datasets under `data/processed/`.

4. **Black-Scholes Pricing**
   - Implement call and put pricing.
   - Support Greeks later if needed.

5. **Implied Volatility**
   - Solve implied volatility numerically from market mid prices.
   - Handle failed solves, no-arbitrage violations, and invalid inputs gracefully.

6. **Historical Volatility**
   - Compute log returns from adjusted close prices.
   - Annualize rolling realized volatility.
   - Compare realized volatility windows with option maturities.

7. **Analysis**
   - Join option-chain implied vol with equity historical volatility.
   - Build summary tables by expiry, strike, and moneyness.

8. **Visualization**
   - Draw volatility smile curves.
   - Draw volatility term structure.
   - Draw volatility surface using strike/moneyness and maturity axes.

## Directory Structure

```text
.
├── README.md
├── pyproject.toml
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
│   └── figures/
├── src/
│   └── bs_pricer/
│       ├── __init__.py
│       ├── analysis.py
│       ├── black_scholes.py
│       ├── cleaning.py
│       ├── config.py
│       ├── data_download.py
│       ├── historical_volatility.py
│       ├── implied_volatility.py
│       ├── plotting.py
│       └── pipeline.py
└── tests/
    ├── test_black_scholes.py
    └── test_implied_volatility.py
```

## Suggested Implementation Order

1. Implement Black-Scholes pricing and unit tests.
2. Implement implied volatility solver and unit tests.
3. Add yfinance data download.
4. Add data cleaning and validation.
5. Add historical volatility calculations.
6. Add comparison analysis.
7. Add smile and surface plotting.
8. Wrap the full flow in `pipeline.py`.

