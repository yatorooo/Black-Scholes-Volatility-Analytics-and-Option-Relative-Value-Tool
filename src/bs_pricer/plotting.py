"""Visualization functions for smiles, term structure, and volatility surfaces."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _iv_data(
    options: pd.DataFrame,
    option_type: str = "call",
    min_moneyness: float = 0.8,
    max_moneyness: float = 1.2,
) -> pd.DataFrame:
    data = options.dropna(subset=["solved_iv"]).copy()
    data = data[data["time_to_expiry"] > 0]
    data = data[data["moneyness"].between(min_moneyness, max_moneyness)]
    data = data[data["option_type"] == option_type]
    return data.sort_values(["expiry", "moneyness"])


def plot_volatility_smile(
    options: pd.DataFrame,
    expiry: str | None = None,
    option_type: str = "call",
    x: str = "moneyness",
):
    """Plot implied volatility against strike or moneyness for one expiry."""
    data = _iv_data(options, option_type=option_type)

    if expiry is None:
        expiry = data["expiry"].min()

    data = data[data["expiry"] == expiry].sort_values(x)

    return px.line(
        data,
        x=x,
        y="solved_iv",
        markers=True,
        title=f"{option_type.title()} Volatility Smile - {expiry}",
        labels={
            x: x.replace("_", " ").title(),
            "solved_iv": "Implied Volatility",
        },
    )


def plot_volatility_surface(
    options: pd.DataFrame,
    option_type: str = "call",
    x: str = "moneyness",
):
    """Plot implied volatility across strike or moneyness and maturity."""
    data = _iv_data(options, option_type=option_type)
    data[x] = data[x].round(3)

    surface = data.pivot_table(
        index="time_to_expiry",
        columns=x,
        values="solved_iv",
        aggfunc="mean",
    ).sort_index()

    fig = go.Figure(
        data=[
            go.Surface(
                x=surface.columns.to_numpy(),
                y=surface.index.to_numpy(),
                z=surface.to_numpy(),
                colorscale="Viridis",
            )
        ]
    )

    fig.update_layout(
        title=f"{option_type.title()} Implied Volatility Surface",
        scene={
            "xaxis_title": x.replace("_", " ").title(),
            "yaxis_title": "Time To Expiry",
            "zaxis_title": "Implied Volatility",
        },
    )

    return fig


def plot_historical_vs_implied():
    """Plot historical volatility against implied volatility."""
    raise NotImplementedError
