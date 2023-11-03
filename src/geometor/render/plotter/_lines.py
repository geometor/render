"""
method implementations for the ``Plotter`` class

- _plot_line
- _plot_selected_line

"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *


def _plot_line(
    plotter: Plotter,
    line: spg.Line,
    classes: list = None,
) -> list[mp.Line2D]:
    """
    returns list of plot artists
    """
    if classes is None:
        classes = []

    ends = plotter.bounds.intersection(line)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = get_styles("line", classes)
    return plotter.ax_main.plot(xs, ys, **styles)


def _plot_selected_line(
    plotter: Plotter,
    line: spg.Line,
    classes: list = None,
) -> list[mp.Line2D]:
    """
    returns list of plot artists
    """
    if classes is None:
        classes = []

    ends = plotter.bounds.intersection(line)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = get_styles("line", classes)
    styles.update(get_styles("line_selected", classes))
    return plotter.ax_main.plot(xs, ys, **styles)


