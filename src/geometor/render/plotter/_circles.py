"""
plot circle functions for renderers
"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *


def _plot_circle(
    plotter: Plotter,
    circle: spg.Circle,
    classes: list = None,
) -> list[plt.Circle]:
    """takes a sympy circle and plots with the matplotlib Circle patch"""
    if classes is None:
        classes = []

    center = (circle.center.x.evalf(), circle.center.y.evalf())
    radius = circle.radius

    styles = get_styles("circle", classes)
    patch = plt.Circle(center, radius, **styles)
    plotter.ax_main.add_patch(patch)
    # TODO: fix return list
    return [patch]


def _plot_selected_circle(
    plotter: Plotter,
    circle: spg.Circle,
    classes: list = None,
) -> list[plt.Circle]:
    if classes is None:
        classes = []

    center = (circle.center.x.evalf(), circle.center.y.evalf())
    radius = circle.radius

    styles = get_styles("circle", classes)
    styles.update(get_styles("circle_selected", classes))
    patch = plt.Circle(center, radius, **styles)
    plotter.ax_main.add_patch(patch)

    # TODO: fix return list
    return [patch]


