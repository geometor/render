"""
functions to plot segments
"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *

#  from geometor.elements.render.plotter.plotter import Plotter


def _plot_segment(
    plotter: Plotter, segment: spg.Segment, style_type: str = None, classes: list = None
) -> list:
    style_type = style_type if style_type else "segment"

    if classes is None:
        classes = []

    xs = [pt.x.evalf() for pt in segment.points]
    ys = [pt.y.evalf() for pt in segment.points]

    styles = get_styles(style_type, classes)
    return plotter.ax_main.plot(xs, ys, **styles)


def _plot_line_segment(plotter: Plotter, line: spg.Line, classes: list = None) -> list:
    return plotter.plot_segment(line, "line_segment", classes)


def _plot_circle_radius(
    plotter: Plotter, radius_segment: spg.Segment, classes: list = None
) -> list:
    return plotter.plot_segment(radius_segment, "circle_radius", classes)
