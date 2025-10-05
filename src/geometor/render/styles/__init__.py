"""
dictionary of style sets for matplotlib
"""

from ._default import _default
from ._red import _red
from ._green import _green
from ._blue import _blue
from .z_levels import *

STYLES = {}
STYLES["default"] = _default
STYLES["red"] = _red
STYLES["green"] = _green
STYLES["blue"] = _blue

def add_styles(styles_dict):
    STYLES.update(styles_dict)

def get_styles(element_type, classes: list = None):
    styles = STYLES["default"].get(element_type).copy()
    # override default with classes
    if classes:
        for class_name in classes:
            if class_name in STYLES:
                styles.update(STYLES[class_name].get(element_type).copy())

    return styles

#  point_inner_color = "w"
#  point_outer_color = "k"
#  point_selected_color = "y"
#  point_highlight_color = "w"
#  STYLES["0"] = {
    #  "point_inner": {
        #  "color": point_inner_color,
        #  "linestyle": "",
        #  "marker": ".",
        #  "markersize": 2,
        #  "zorder": Z_POINT_INNER,
    #  },
    #  "point_outer": {
        #  "color": "k",
        #  "linestyle": "",
        #  "marker": ".",
        #  "markersize": 8,
        #  "zorder": Z_POINT_OUTER,
    #  },
    #  "point_selected": {
        #  #  "color": point_selected_color,
        #  #  "linestyle": "",
        #  #  "fillstyle": "none",
        #  #  "marker": "o",
        #  #  "markersize": 40,
        #  #  "markeredgecolor": "y",
        #  #  "markeredgewidth": 2,
        #  #  "zorder": Z_SELECTED,
    #  },
    #  "point_highlight": {
        #  "color": "r",
        #  "linestyle": "",
        #  "marker": "o",
        #  "markersize": 30,
        #  "markeredgecolor": "r",
        #  "markeredgewidth": 10,
        #  "zorder": Z_POINT_HILITE,
    #  },
#  }




#  STYLES['given'] = {'color':'#FFF6', 'markersize':7, 'marker':'o'}

#  STYLES['guide'] = {'color':'#333', 'linestyle':':'}

#  STYLES['blue'] = {'color':'#66F', 'linestyle':':'}
#  STYLES['green'] = {'color':'#2F2', 'linestyle':':'}
#  STYLES['pappus'] = {'linestyle':'--'}
#  STYLES['pink'] = {'color':'#F99', 'linestyle':'--'}
#  STYLES['bisector'] = {'linestyle':'-.'}

#  STYLES['set1'] = {'color':'#09C', 'linestyle':':'}
#  STYLES['set1pt'] = {'color':'#09C', 'markersize':8, 'marker':'o'}

#  STYLES['set2'] = {'color':'#C33', 'linestyle':':'}
#  STYLES['set2pt'] = {'color':'#C33', 'markersize':8, 'marker':'o'}

#  STYLES['ring'] = {'color':'#4444', 'linestyle':'-'}

#  STYLES['gold'] = {'color':'#C90', 'linestyle':':'}
#  STYLES['goldpt'] = {'color':'#C90', 'markersize':8, 'marker':'o'}


#  STYLES['circle'] = {'color':'#0FF', 'markersize':7, 'marker':'o'}
#  STYLES['square'] = {'color':'#FF0', 'markersize':7, 'marker':'s'}
#  STYLES['diamond'] = {'color':'#F0F', 'markersize':7, 'marker':'D'}
#  STYLES['star'] = {'color':'#F99', 'markersize':12, 'marker':'*'}

#  STYLES['nine'] = {'edgecolor':'#3F06', 'facecolor':'#3F03', 'linestyle':'-', 'linewidth':1}
#  STYLES['yellow'] = {'edgecolor':'#FF09', 'facecolor':'#FF03', 'linestyle':'-', 'linewidth':1}
#  STYLES['cyan'] = {'color':'#0FF3', 'linestyle':'-'}
#  STYLES['cyanpt'] = {'color':'#C90', 'markersize':8, 'marker':'o'}
#  STYLES['magenta'] = {'color':'#F0F3', 'linestyle':'-'}
