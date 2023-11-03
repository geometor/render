"""
matplotlib styles - blue
"""

from .z_levels import *

_blue = {
    'line': {
        'color': '#33F',
        #  'linestyle': ':',
        #  'linewidth': 1.5
    },
    'line_segment': {
        'color': '#33F9',
        #  'linestyle': '-',
        #  'linewidth': 5
    },
    "line_selected": {
        "linestyle": "-",
        "zorder": Z_SELECTED,
    },
    'circle': {
        'edgecolor': '#33F',
        'facecolor': '#00000000',
        #  'linestyle': ':',
        #  'linewidth': 1.5,
        #  'fill': False
    },
    'circle_segment': {
        'edgecolor': '#33F9',
        #  'linestyle': '-',
        #  'linewidth': 5,
    },
    'segment': {
        'color':  '#33F9',
        #  'linestyle': '-',
        #  'linewidth': 5,
        #  'marker': '',
        #  'markersize': 0,
    }
}
