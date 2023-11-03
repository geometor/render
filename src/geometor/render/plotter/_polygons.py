"""
polygons module
===============

functions to plot polygons
"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *


def _plot_polygon(
        plotter: Plotter,
        poly: spg.Polygon, 
        classes: list = None,
    ):
    '''takes a sympy Polygon and plots with the matplotlib Polygon patch'''
    if classes is None:
        classes = []

    if isinstance(poly, spg.Segment2D):
        return self.plot_segment2(poly)
    else:
        if isinstance(poly, list):
            # Triangles are a list!?
            xy = [(pt[0].evalf(), pt[1].evalf()) for pt in poly[0].vertices]
        else:
            xy = [(pt.x.evalf(), pt.y.evalf()) for pt in poly.vertices]

        styles = get_styles("polygon", classes)
        patch = plt.Polygon(xy, **styles)
        plotter.ax_main.add_patch(patch)
        return [patch]




