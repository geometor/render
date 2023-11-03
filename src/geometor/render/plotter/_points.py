"""
functions to plot points
"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *

from sympy.geometry.point import Point as sp_Point


def _plot_point(
    plotter: Plotter,
    pt: sp_Point,
    label: str,
    classes: list = None,
) -> list:
    """plot the point with corresponding styles
    returns a list of artists
    """

    if classes is None:
        classes = []

    main_artists = []

    # collect x, y values into separate arrays
    xs = [pt.x.evalf()]
    ys = [pt.y.evalf()]

    # plots the corresponding black underdot to separate the white dot from the
    # intersecting structs
    styles = get_styles("point_outer", classes)
    main_artists.append(
        plotter.ax_main.plot(
            xs,
            ys,
            **styles,
        )[0]
    )

    # plots the inner white dot by default
    styles = get_styles("point_inner", classes)
    main_artists.append(
        plotter.ax_main.plot(
            xs,
            ys,
            **styles,
        )[0]
    )

    # plot highlight
    if classes:
        styles = get_styles("point_highlight", classes)
        main_artists.append(
            plotter.ax_main.plot(
                xs,
                ys,
                **styles,
            )[0]
        )

    #  return pt_inner, pt_outer, pt_highlight
    #  inspect(main_artists)
    return main_artists


def _plot_selected_points(
    plotter: Plotter,
    pts: list[spg.Point],
) -> list:
    xs = [pt.x.evalf() for pt in pts]
    ys = [pt.y.evalf() for pt in pts]

    styles = get_styles("point_selected")
    return plotter.ax_main.plot(xs, ys, **styles)


def _plot_circle_points(
    plotter: Plotter,
    pts: list[spg.Point],
) -> list:
    xs = [pt.x.evalf() for pt in pts]
    ys = [pt.y.evalf() for pt in pts]

    styles = get_styles("circle_points")
    return plotter.ax_main.plot(xs, ys, **styles)
