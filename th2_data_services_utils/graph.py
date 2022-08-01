from typing import List, Optional

import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame


def create_tick_diagram(
        data: DataFrame, legend_to_table: bool = False
) -> Optional[DataFrame]:
    """Create ticks diagram.

    Args:
        data: Data.
        legend_to_table: Whether to create legend in Dataframe.
    """
    fig = go.Figure()

    table = []
    if legend_to_table:
        for index, (element, payload) in enumerate(data.items()):
            fig.add_trace(
                go.Scatter(
                    name=index,
                    x=list(payload.keys()),
                    y=list(payload.values),
                    mode="lines",
                )
            )
            table.append({"index": index, "name": element})
    else:
        for element, payload in data.items():
            fig.add_trace(
                go.Scatter(
                    name="_".join(element) if not isinstance(element, str) else element,
                    x=list(payload.keys()),
                    y=list(payload.values),
                    mode="lines",
                )
            )

    fig.show()

    if legend_to_table:
        return DataFrame(table)


def create_line_plot_image(
        x: List[int],
        y: List[int],
        file_name: str = "file",
        x_label: str = None,
        y_label: str = None,
        xticks_label: List[str] = None,
        title: str = "plot",
        width: int = None,
        height: int = None
) -> None:
    """Creates Line plot as file.

    Args:
        x: Values of X-axis.
        y: Values of Y-axis.
        file_name: Output file name.
        x_label: Label of X-axis.
        y_label: Label of Y-axis.
        title: Title of plot.
        xticks_label: Values for X axis.
        width: Width
        height: Height
    """
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()
    if width is not None and height is not None:
        fig.set_size_inches(width, height)

    ax.plot(x, y)
    ax.grid()
    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    if xticks_label is not None:
        plt.xticks(x, xticks_label, rotation="vertical")

    fig.savefig(f"{file_name}.png")
