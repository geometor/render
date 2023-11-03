"""
matplotlib styles - default
"""
from .z_levels import *

point_inner_color = "w"
point_outer_color = "k"
point_selected_color = "y"
point_highlight_color = "w"
line_color = "#999"
line_segment_color = "#9999"
circle_color = "#C09"

_default = {
    "point_inner": {
        "color": point_inner_color,
        "linestyle": "",
        "marker": ".",
        "markersize": 5,
        "zorder": Z_POINT_INNER,
    },
    "point_outer": {
        "color": point_outer_color,
        "linestyle": "",
        "marker": ".",
        "markersize": 8,
        "zorder": Z_POINT_OUTER,
    },
    "point_highlight": {
        "color": point_highlight_color,
        "linestyle": "",
        "marker": "o",
        "markersize": 8,
        "zorder": Z_POINT_HILITE,
    },
    "point_selected": {
        "color": point_selected_color,
        "linestyle": "",
        "fillstyle": "none",
        "marker": "o",
        "markersize": 15,
        "markeredgecolor": "y",
        "markeredgewidth": 2,
        "zorder": Z_SELECTED,
    },
    "line": {"color": line_color, "linestyle": ":", "linewidth": 1.5, "zorder": Z_LINE},
    "line_selected": {
        "linestyle": "-",
        "zorder": Z_SELECTED,
    },
    "line_segment": {
        "color": line_segment_color,
        "linestyle": "-",
        "linewidth": 5,
        "zorder": Z_SELECTED,
    },
    "circle": {
        "edgecolor": circle_color,
        "facecolor": "#00000000",
        "linestyle": ":",
        "linewidth": 1.5,
        "fill": False,
        "zorder": Z_CIRCLE,
    },
    "circle_selected": {
        "linestyle": "-",
        "zorder": Z_SELECTED,
    },
    "circle_points": {
        "color": circle_color,
        "linestyle": "",
        "fillstyle": "none",
        "marker": "o",
        "markersize": 15,
        "markeredgecolor": circle_color,
        "markeredgewidth": 2,
        "zorder": Z_POINT_HILITE,
    },
    "circle_radius": {
        "color": circle_color,
        "linestyle": "-",
        "linewidth": 5,
        "marker": "",
        "markersize": 0,
        "zorder": Z_SELECTED,
    },
    "segment": {
        "color": "#fc09",
        "fillstyle": "none",
        "linestyle": "-",
        "linewidth": 5,
        "solid_capstyle": "round",
        "marker": "o",
        "markersize": 15,
        "markeredgecolor": "#fc09",
        "markerfacecolor": "#0000",
        "markeredgewidth": 2,
        "zorder": Z_SEGMENT,
    },
    "polygon": {
        "edgecolor": "#36c9",
        "facecolor": "#36c3",
        "fill": True,
        "linestyle": "-",
        "linewidth": 1,
        "zorder": Z_POLYGON,
        #  'marker': '',
        #  'markersize': 0,
    },
    "wedge": {
        "edgecolor": "#36c9",
        "facecolor": "#36c3",
        "fill": True,
        "linestyle": "-",
        "linewidth": 1,
        "zorder": Z_POLYGON,
        #  'marker': '',
        #  'markersize': 0,
    },
}
