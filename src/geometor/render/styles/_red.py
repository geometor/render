"""
matplotlib styles - red
"""

from .z_levels import *

_color = "#F33"
_tint = "#F336"

_red = {
    'line': {
        'color': _color,
    },
    'line_segment': {
        'color': _tint,
    },
    "line_selected": {
        "linestyle": "-",
    },
    'circle': {
        'edgecolor': _color,
    },
    'circle_segment': {
        'edgecolor': _tint,
    },
    'segment': {
        'color': _tint,
    },
    "polygon": {
        "edgecolor": _color,
        "facecolor": _tint,
        #  'marker': '',
        #  'markersize': 0,
    },
}
