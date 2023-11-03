"""
matplotlib styles - green
"""

from .z_levels import *

_green = {
    'line': {
        'color': '#3F3',
        #  'linestyle': ':',
        #  'linewidth': 1.5
    },
    'line_segment': {
        'color': '#3F39',
        #  'linestyle': '-',
        #  'linewidth': 5
    },
    "line_selected": {
        "linestyle": "-",
        "zorder": Z_SELECTED,
    },
    'circle': {
        'edgecolor': '#3F3',
        'facecolor': '#00000000',
        #  'linestyle': ':',
        #  'linewidth': 1.5,
        #  'fill': False
    },
    'circle_segment': {
        'edgecolor': '#3F39',
        #  'linestyle': '-',
        #  'linewidth': 5,
    },
    'segment': {
        'color':  '#3F39',
        #  'linestyle': '-',
        #  'linewidth': 5,
        #  'marker': '',
        #  'markersize': 0,
    }
}
