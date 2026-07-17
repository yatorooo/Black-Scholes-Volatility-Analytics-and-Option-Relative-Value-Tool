"""Visualization functions for smiles, term structure, and volatility surfaces."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata


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
    grid_size: int = 60,
):
    """Plot implied volatility across strike or moneyness and maturity.

    The raw solved IVs sit at irregular, sparse (x, time_to_expiry) points, so
    they are interpolated onto a dense regular grid before surfacing --
    plotting the raw points directly as a grid leaves most cells empty and
    renders as a torn, holey mesh.
    """
    data = _iv_data(options, option_type=option_type)
    points = data.groupby(["time_to_expiry", x], as_index=False)["solved_iv"].mean()

    x_grid = np.linspace(points[x].min(), points[x].max(), grid_size)
    y_grid = np.linspace(points["time_to_expiry"].min(), points["time_to_expiry"].max(), grid_size)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)

    z_mesh = griddata(
        points=(points[x].to_numpy(), points["time_to_expiry"].to_numpy()),
        values=points["solved_iv"].to_numpy(),
        xi=(x_mesh, y_mesh),
        method="linear",
    )

    fig = go.Figure(
        data=[
            go.Surface(
                x=x_grid,
                y=y_grid,
                z=z_mesh,
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
