"""
plot wedges functions for renderers

.. todo:: complete integration of wedges
"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *

from geometor.model import Wedge

from rich import inspect


def _plot_wedge(
    plotter: Plotter,
    wedge: Wedge,
    classes: list = None,
) -> list[mp.patch.Wedge]:
    """takes a geometor.model.Wedge and maps it to a matplotlib patch"""
    if classes is None:
        classes = []

    pt_center = wedge.circle.center
    center = (float(pt_center.x.evalf()), float(pt_center.y.evalf()))
    rad_val = float(wedge.circle.radius.evalf())
    base_line = spg.Line(pt_center, spg.Point(pt_center.x + 1, pt_center.y))

    # t = polygon
    a1 = math.degrees(base_line.angle_between(wedge.start_ray).evalf())
    a2 = math.degrees(base_line.angle_between(wedge.sweep_ray).evalf())
    cy = center[1]
    p1y = float(wedge.start_point.y.evalf())
    if cy > p1y:
        a1 = -a1
    p2y = float(wedge.end_point.y.evalf())
    if cy > p2y:
        a2 = -a2

    styles = get_styles("wedge", classes)
    patch = mp.patches.Wedge(
        center,
        rad_val,
        a1,
        a2,
        **styles,
    )

    patch = plotter.ax_main.add_patch(patch)
    return [patch]




