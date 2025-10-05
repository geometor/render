## src/geometor/render/__init__.py

```py
"""
The Render Module
provides functions for plotting elements from the geometric model to
matplotlib.
"""
__author__ = "geometor"
__maintainer__ = "geometor"
__email__ = "github@geometor.com"
__version__ = "0.0.1"
__licence__ = "MIT"

from .common import *

from geometor.model import *
from geometor.model.utils import *

from .utils import *

from .plotter import *
from .sections import *
from .chains import *
from .groups import *
from .sequencer import *
from .titler import *


```

## src/geometor/render/plotter/__init__.py

```py

from __future__ import annotations

from ..common import *
from ..styles import *

from ._points import (
    _plot_point,
    _plot_selected_points,
    _plot_circle_points,
)
from ._lines import _plot_line, _plot_selected_line
from ._circles import _plot_circle, _plot_selected_circle
from ._segments import _plot_segment, _plot_line_segment, _plot_circle_radius
from ._polygons import _plot_polygon
from ._wedges import _plot_wedge, Wedge

from ._elements import _plot_element, PlotElement

from geometor.model import Model
from geometor.render.utils import *


class Plotter:
    """
    The Plotter class handles the fundametals for rendering a geometric construction

    parameters
    ----------
    - ``name`` : :class:`str`: establish name for the model instance

    attributes
    ----------
    - :attr:`plot_name` -> :class:`str`: name of the model
    - :attr:`margin` -> :class:`float`: margin for the plot
    - :attr:`FIG_W` -> :class:`int`: width of the figure
    - :attr:`FIG_H` -> :class:`int`: height of the figure
    - :attr:`ax_main` -> :class:`matplotlib.axes.Axes`: Axes for the main graph
    - :attr:`ax_header` -> :class:`matplotlib.axes.Axes`: Axes for the header panel
    - :attr:`ax_footer` -> :class:`matplotlib.axes.Axes`: Axes for the footer panel
    - :attr:`figure` -> :class:`matplotlib.figure.Figure`: the main figure of the plot

    methods
    -------
    - :meth:`plot_point` -> :class:`Point <sympy.geometry.point.Point>`
    - :meth:`plot_line` -> :class:`Line <sympy.geometry.line.Line>`
    - :meth:`plot_circle` -> :class:`Circle <sympy.geometry.ellipse.Circle>`
    """

    def __init__(
        self,
        plot_name: str = None,
        margin_ratio=0.1,
        FIG_W=16,
        FIG_H=9,
    ):
        """
        Initializes the Sequencer with the given model and optional parameters.
        Sets up the figure size, style, and layout using Matplotlib.

        Args:
            model (Model): The geometric model to be processed and plotted.
            plot_name (str, optional): An optional name for the plot.
            margin (float, optional): An optional parameter to control the margins of the plot.
        """
        self.plot_name = plot_name

        self.margin_ratio = margin_ratio

        plt.rcParams["figure.figsize"] = [FIG_W, FIG_H]
        plt.style.use("dark_background")
        custom_preamble = {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{amsmath} \usepackage{xcolor}",  # for the align enivironment
        }
        plt.rcParams.update(custom_preamble)

        self.FIG_H = FIG_H
        self.FIG_W = FIG_W

        self.fig, (self.ax_header, self.ax_main, self.ax_footer) = plt.subplots(
            3, 1, gridspec_kw={"height_ratios": [1, 10, 1]}
        )
        plt.tight_layout()

        self.reset_ax_all()

        self.cursor = mplcursors.cursor()
        self.cursor_points = []

        self.plot_elements = []

    def add_styles(self, styles: dict):
        add_styles(styles)

    def reset_ax_all(self) -> None:
        self.reset_ax_main()
        self.reset_ax_header()
        self.reset_ax_footer()

    def reset_ax_main(self) -> None:
        self.ax_main.clear()
        self.ax_main.axis(False)
        self.ax_main.set_aspect("equal")

    def reset_ax_header(self) -> None:
        self.ax_header.clear()
        self.ax_header.axis(False)

    def reset_ax_footer(self) -> None:
        self.ax_footer.clear()
        self.ax_footer.axis(False)

    def set_ax_main_bounds(self, bounds):
        vmin = bounds.vertices[0]
        vmax = bounds.vertices[2]

        self.ax_main.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
        self.ax_main.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
        # TODO: not sure if this should be here
        self.ax_main.invert_yaxis()

    def annotate_point(self, point: spg.Point, text):
        """Annotate the given point with the provided text on the given axes."""
        x = point.x.evalf()
        y = point.y.evalf()
        styles = {
            "fontsize": 12,
            "xytext": (8, 8),
            "textcoords": "offset points",
        }
        return [self.ax_main.annotate(text, (x, y), **styles)]

    plot_point = _plot_point
    plot_selected_points = _plot_selected_points
    plot_circle_points = _plot_circle_points

    plot_line = _plot_line
    plot_selected_line = _plot_selected_line

    plot_circle = _plot_circle
    plot_selected_circle = _plot_selected_circle

    plot_segment = _plot_segment
    plot_line_segment = _plot_line_segment
    plot_circle_radius = _plot_circle_radius

    plot_polygon = _plot_polygon

    plot_wedge = _plot_wedge

    plot_element = _plot_element

    def plot_model(self, model: Model, annotate_points=False):
        x_limits, y_limits = model.limits()
        x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
        x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(
            x_limits, y_limits
        )

        self.bounds = spg.Polygon(
            spg.Point(x_limits[0], y_limits[1]),
            spg.Point(x_limits[0], y_limits[0]),
            spg.Point(x_limits[1], y_limits[0]),
            spg.Point(x_limits[1], y_limits[1]),
        )
        self.set_ax_main_bounds(self.bounds)

        self.plot_header(model.name)

        self.cursor_points = {}

        for i, (el, details) in enumerate(model.items()):
            if isinstance(el, spg.Point):
                pt_inner, *pts = self.plot_point(
                    el, details.label, details.classes, 
                )
                details.pt = el
                self.cursor_points[pt_inner] = details
                if annotate_points:
                    self.annotate_point(el, details.label)

            if isinstance(el, spg.Line):
                self.plot_line(el, details.classes)

            if isinstance(el, spg.Circle):
                self.plot_circle(el, details.classes)

            if isinstance(el, spg.Segment):
                self.plot_segment(el, details.classes)

            if isinstance(el, spg.Polygon):
                self.plot_polygon([el], details.classes)

            if isinstance(el, Wedge):
                self.plot_wedge(el, details.classes)

        def _on_add(sel):
            details = self.cursor_points[sel.artist]

            xval = sp.latex(details.pt.x)
            yval = sp.latex(details.pt.y)
            sel.annotation.set_text(f"{details.label}:\nx: ${xval}$\ny: ${yval}$")
            sel.annotation.set(
                color="k",
                fontsize="x-large",
                bbox=dict(boxstyle="round,pad=0.5", fc="w"),
            )
            sel.annotation.arrow_patch.set(arrowstyle="simple", ec="k", fc="w")

        self.cursor = mplcursors.cursor(self.cursor_points, hover=True)
        self.cursor.connect("add", _on_add)

    def plot_header(self, text):
        """
        sets up one panel for header
        """
        self.reset_ax_header()

        artist = self.ax_header.text(
            0.5,
            0.5,
            text,
            ha="center",
            va="center",
            fontdict={"color": "w", "size": "20"},
        )
        return [artist]

    def plot_footer(self, index, description, label):
        """
        sets up 3 panels in footer for index, description and label
        """
        
        #  self.reset_ax_footer()

        index_artist = self.ax_footer.text(
            0, 0.5, index, ha="left", va="center", fontdict={"color": "r", "size": "24"}
        )
        description_artist = self.ax_footer.text(
            0.5,
            0.5,
            description,
            ha="center",
            va="center",
            fontdict={"color": "w", "size": "20"},
        )
        #  if label:
        #  label = f"${label}$"
        label_artist = self.ax_footer.text(
            1,
            0.5,
            label,
            ha="right",
            va="center",
            fontdict={"color": "w", "size": "24"},
        )

        return [index_artist, description_artist, label_artist]

    def _add_margin_to_ax_main_limits(
        self, x_limits: list, y_limits: list, default_margin=0.5
    ):
        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]

        if x_range:
            x_margin = x_range * self.margin_ratio
            if y_range:
                y_margin = y_range * self.margin_ratio
            else:
                y_margin = x_margin
        else:
            if y_range:
                y_margin = y_range * self.margin_ratio
                x_margin = y_margin
            else:
                x_margin = default_margin
                y_margin = default_margin

        x_limits[0] -= x_margin
        x_limits[1] += x_margin

        y_limits[0] -= y_margin
        y_limits[1] += y_margin

        return x_limits, y_limits

    def _pad_ax_main_limits_for_aspect_ratio(self, x_limits: list, y_limits: list):
        current_width = x_limits[1] - x_limits[0]
        current_height = y_limits[1] - y_limits[0]

        current_ratio = current_width / current_height
        # TODO: the height proportion of 10/12 should be set when
        # configuring the axes.
        ax_main_ratio = self.FIG_W / (self.FIG_H * (10 / 12))

        if current_ratio < ax_main_ratio:
            # Increase width
            extra_width = (current_height * ax_main_ratio) - current_width
            x_limits[0] -= extra_width / 2
            x_limits[1] += extra_width / 2
        elif current_ratio > ax_main_ratio:
            # Increase height
            extra_height = (current_width / ax_main_ratio) - current_height
            y_limits[0] -= extra_height / 2
            y_limits[1] += extra_height / 2

        return x_limits, y_limits

    def set_plotter_limits_from_points(self, points):
        # TODO: this should not change the self.bounds - especially if used for zoom
        x_limits, y_limits = get_limits_from_points(points)
        x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
        x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(
            x_limits, y_limits
        )

        self.bounds = spg.Polygon(
            spg.Point(x_limits[0], y_limits[1]),
            spg.Point(x_limits[0], y_limits[0]),
            spg.Point(x_limits[1], y_limits[0]),
            spg.Point(x_limits[1], y_limits[1]),
        )
        self.set_ax_main_bounds(self.bounds)


    def zoom_to_points(self, zoom_pts):
        if zoom_pts:
            x_limits, y_limits = get_limits_from_points(zoom_pts)
            x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
            x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(
            x_limits, y_limits
            )

            self.ax_main.set_xlim(x_limits[0], x_limits[1])
            self.ax_main.set_ylim(y_limits[0], y_limits[1])

    def zoom_to_bounds(self):
        self.set_ax_main_bounds(self.bounds)



```

## src/geometor/render/sequencer/__init__.py

```py
from __future__ import annotations

from ..common import *
from ..styles import *

from ._plot import _plot_sequence
from ._step import _step_sequence


from ..plotter import Plotter

class Sequencer(Plotter):
    """
    The Sequencer class encapsulates the setup and generation of geometric
    plots.  It receives a geometric model and provides functionalities to
    sequence and render the plot.

    parameters:
        ``plot_name`` : :class:`str`
            the name of the plot
            
    attributes:
        plot_name (str, optional): An optional name for the plot.
        margin (float, optional): An optional parameter to control the margins of the plot.
        fig (Figure): Matplotlib figure object.
        ax (Axes): Matplotlib axes object for the main plot.
        ax_label (Axes): Matplotlib axes object for the label.
    """
    def __init__(
        self,
        plot_name: str = None,
        margin=0.1,
        FIG_W=16,
        FIG_H=9,
    ):
        """
        Initializes the Sequencer with the given model and optional parameters.
        Sets up the figure size, style, and layout using Matplotlib.

        Args:
            model (Model): The geometric model to be processed and plotted.
            plot_name (str, optional): An optional name for the plot.
            margin (float, optional): An optional parameter to control the margins of the plot.
        """
        super().__init__(plot_name, margin, FIG_W, FIG_H)
        self.selected = []


    plot_sequence = _plot_sequence
    #  animate_sequence = _animate_sequence
    step_sequence = _step_sequence


```

## src/geometor/render/styles/__init__.py

```py
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

```

## src/geometor/render/titler/__init__.py

```py
from __future__ import annotations

from ..common import *
from ..styles import *
from ..utils import *

#  from .._html import _create_html_page

#  from ._sequences import _plot_sequence

from ..plotter import Plotter


class Titler(Plotter):
    """
    The Titler class is primarily for creating slides with latex rendered or overlays

    parameters:
        ``plot_name`` : :class:`str`
            the name of the plot

    attributes:
        model (Model): The geometric model to be processed and plotted.
        plot_name (str, optional): An optional name for the plot.
        margin (float, optional): An optional parameter to control the margins of the plot.
        fig (Figure): Matplotlib figure object.
        ax (Axes): Matplotlib axes object for the main plot.
        ax_label (Axes): Matplotlib axes object for the label.
    """

    def __init__(
        self,
        model: Model = None,
        plot_name: str = None,
        margin=0.1,
        FIG_W=16,
        FIG_H=9,
    ):
        """
        Initializes the Sequencer with the given model and optional parameters.
        Sets up the figure size, style, and layout using Matplotlib.

        Args:
            model (Model): The geometric model to be processed and plotted.
            plot_name (str, optional): An optional name for the plot.
            margin (float, optional): An optional parameter to control the margins of the plot.
        """
        super().__init__(plot_name, margin, FIG_W, FIG_H)

    def plot_title(self, title, folder, filename, color="w", size=44):
        """TODO: Docstring for plot_title.

        :title: TODO
        :returns: TODO

        """
        folder = os.path.abspath(folder)
        os.makedirs(folder, exist_ok=True)

        self.reset_ax_main()
        self.ax_main.text(
            0.5,
            0.5,
            title,
            ha="center",
            va="center",
            fontdict={"color": color, "size": size},
        )

        return snapshot_2(folder, filename)
        #  plt.show()

    def plot_overlay(self, title, folder, filename, color="w", size=44):
        """TODO: Docstring for plot_overlay.

        :title: TODO
        :returns: TODO

        """
        folder = os.path.abspath(folder)
        os.makedirs(folder, exist_ok=True)

        fontdict = {"family": "Fira Sans Condensed", "color": color, "size": size}

        fig, ax = plt.subplots(1, 1)
        plt.tight_layout()
        ax.axis("off")
        ax.set_aspect("equal")
        ax.clear()
        ax.axis(False)
        ax.text(
            0.15,
            0.8,
            title,
            ha="center",
            va="top",
            fontdict={"color": color, "size": size},
        )

        return snapshot_2(folder, filename, transparent=True)
        #  plt.show()


```

## src/geometor/render/__main__.py

```py
"""The package entry point into the application."""

from .app import run

if __name__ == "__main__":
    run()
```

## src/geometor/render/_html.py

```py
import os
from pathlib import Path

def _create_html_page(svg_files, output_path="steps/index.html"):
    # HTML head content
    head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Steps</title>
        <style>
html {
    background: black;
}
.steps {
    width: 100%;
    height: 100vh; /* Takes full viewport height */
    position: relative;
}

.steps > object {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0; /* Initially hide all SVGs */
    transition: opacity 0.05s ease; /* Transition effect */
}
    </style>
    </head>
    <body>
    """

    # HTML navigation buttons
    #  <button onclick="previousSVG()">Previous</button>
    #  <button onclick="nextSVG()">Next</button>
    navigation = """
        <div class="steps">
    """

    # Embedding the SVGs
    svg_content = ""
    for svg_file in svg_files:
        svg_rel_path = os.path.relpath(svg_file)
        svg_content += f'        <object type="image/svg+xml" data="./{svg_rel_path}"></object>\n'

    # HTML navigation script
    script = """
        </div>
        <script>
            const svgs = document.querySelectorAll('.steps > object');
            let current = 0;

            function showSVG(index) {
                svgs.forEach((svg, i) => {
                    if (i === index) {
                        svg.style.opacity = 1; // Show current SVG
                    } else {
                        svg.style.opacity = 0; // Hide other SVGs
                    }   
                });
            }

            function nextSVG() {
                console.log('next');
                current = (current + 1) % svgs.length;
                showSVG(current);
            }

            function previousSVG() {
                console.log('prev');
                current = (current - 1 + svgs.length) % svgs.length;
                showSVG(current);
            }

            showSVG(current);

            document.addEventListener('keydown', function(event) {
                switch (event.key) {
                    case 'j':
                        nextSVG();
                        break;
                    case 'k':
                        previousSVG();
                        break;
                    case 'g':
                        current = 0;
                        showSVG(current);
                        break;
                    case 'G':
                        current = svgs.length - 1;
                        showSVG(current);
                        break;
                }
            });

        </script>
        </body>
        </html>
    """

    # Combining all parts
    html_content = head + navigation + svg_content + script

    # Saving the HTML file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(html_content)

    return f"HTML page created at {output_path}"



```

## src/geometor/render/app.py

```py
"""
run the main app
"""
from .render import Render


def run() -> None:
    reply = Render().run()
    print(reply)

```

## src/geometor/render/chains.py

```py

from .common import *
from geometor.model import *
from geometor.render import *


def plot_chain(plotter: Plotter, model: Model, index, chain, extensions=["svg", "png"]):
    """
    plot the chain then remove it
    """
    files = []
    selected = []

    # annotate points
    for pt in chain.points:
        label = model[pt].label
        selected.append(plotter.annotate_point(pt, label))

    selected.append(plotter.plot_selected_points(chain.points))

    #  for segment in chain.segments:
    for segment, fib_label in zip(chain.segments, chain.fibonacci_labels):  
    
        selected.append(plotter.plot_segment(segment, classes=[fib_label]))

    # TODO: add flow visualization using arrows or annotations 

    # TODO: add symmetry lines visualization 

    description = "Chain Description"  # You can customize the description here
    label = f"Chain_{index}"  # Customizing the label for the chain

    plotter.plot_footer(index, description, label)

    folder = f"./{plotter.plot_name}/chains"
    filename = f"{index:05}"

    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}.{ext}"))

    # zoom around chain points
    chain_pts = chain.points
    x_limits, y_limits = get_limits_from_points(chain_pts)
    x_limits, y_limits = plotter._add_margin_to_ax_main_limits(x_limits, y_limits)
    x_limits, y_limits = plotter._pad_ax_main_limits_for_aspect_ratio(x_limits, y_limits)

    plotter.ax_main.set_xlim(x_limits[0], x_limits[1])
    plotter.ax_main.set_ylim(y_limits[0], y_limits[1])

    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}-zoom.{ext}"))

    for select in selected:
        selected_el = select.pop(0)
        selected_el.remove()

    # reset view after zoom
    plotter.set_ax_main_bounds(plotter.bounds)

    return files


def plot_chains(plotter: Plotter, model: Model, chains: list, extensions=["svg", "png"]):
    chain_pts = []  # Collecting all points in all chains
    for chain in chains:
        chain_pts.extend(chain.points)

    plotter.set_plotter_limits_from_points(chain_pts)

    files = []

    for index, chain in enumerate(chains):
        files.extend(plot_chain(plotter, model, index, chain))

    return files


```

## src/geometor/render/colors.py

```py
'''
colors module
=============

functions for working with color
'''
from .common import *

def get_colors(cmap_name, steps):
    '''
    return a list of colors n regular steps from a colormap
    '''
    cmap = mp.cm.get_cmap(cmap_name)
    colors = []
    offset = 1 / (2 * steps)
    for step in range(steps):
        color_scale = (((step + offset) % steps) / steps)
        #  color_scale = color_scale + (1 / (color_cycle * 2))
        #  if rev:
            #  color_scale = 1 - color_scale
        colors.append(cmap(color_scale))
    return colors


```

## src/geometor/render/common.py

```py
from rich import print, inspect

import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg
from sympy.abc import x, y

import matplotlib as mp
import matplotlib.pyplot as plt
import mplcursors

import math as math
import numpy as np

from itertools import permutations, combinations
from collections import defaultdict
import logging

from multiprocessing import Pool, cpu_count

from geometor.model.utils import *
from geometor.model import Model

```

## src/geometor/render/groups.py

```py
"""
functions to plot groupings of sections
"""

from .common import *
from geometor.model import *
from geometor.render import *


def plot_group(plotter: Plotter, model: Model, index, group, description, extensions=["svg", "png"]):
    """
    Plot the group then remove it.
    """
    files = []
    selected = []

    # Assuming each group is a list of Sections
    for section in group:
        # Annotate points
        for pt in section.points:
            label = model[pt].label
            selected.append(plotter.annotate_point(pt, label))

        # Highlight points in the section
        selected.append(plotter.plot_selected_points(section.points))

        # Highlight segments in the section
        for segment in section.segments:
            selected.append(plotter.plot_segment(segment))

    # TODO: Add additional visualizations as needed (e.g., flow, symmetry lines)

    label = ""

    plotter.plot_footer(index, description, label)

    folder = f"./{plotter.plot_name}/groups"
    filename = f"{index:05}"

    # Save plot in different formats
    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}.{ext}"))

    # Clean up the annotations and highlights
    for select in selected:
        selected_el = select.pop(0)
        selected_el.remove()

    return files


def plot_groups(
        plotter: Plotter, model: Model, groups: dict, title: str, extensions=["svg", "png"]
):
    all_pts = []  # Collecting all points in all groups

    # Assuming each group value is a list of Sections
    for group in groups.values():
        for section in group:
            all_pts.extend(section.points)

    plotter.set_plotter_limits_from_points(all_pts)

    title = f"{model.name}\n{title}"
    plotter.plot_header(title)

    files = []

    for index, (key, group) in enumerate(groups.items()):
        files.extend(plot_group(plotter, model, index, group, str(key), extensions))

    return files

```

## src/geometor/render/plotter/_circles.py

```py
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



```

## src/geometor/render/plotter/_elements.py

```py
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *

from ._points import (
    _plot_point,
    _plot_selected_points,
    _plot_circle_points,
)
from ._lines import _plot_line, _plot_selected_line
from ._circles import _plot_circle, _plot_selected_circle
from ._segments import _plot_segment, _plot_line_segment, _plot_circle_radius
from ._polygons import _plot_polygon
from ._wedges import _plot_wedge, Wedge


class PlotElement:
    """
    The PlotElement class contains the matplotlib artists for rendering
    a geometric element in matplotlib

    """

    def __init__(
        self,
        main_artists: list = None,
        selected_artists: list = None,
        annotation_artists: list = None,
    ):
        if isinstance(main_artists, list):
            self.main_artists = main_artists
        else:
            if main_artists:
                self.main_artists = [main_artists]
            else:
                self.main_artists = []

        self.selected_artists = selected_artists if selected_artists else []
        self.annotation_artists = annotation_artists if annotation_artists else []
        self.related_elements = []
        self.parent_elements = []
        self.footer_artists = []
        self.label = None
        self.description = None
        self.zoom_pts = []

    def show(self):
        for artist in self.main_artists:
            artist.set_visible(True)

    def hide(self):
        for artist in self.main_artists:
            artist.set_visible(False)
        for artist in self.selected_artists:
            artist.set_visible(False)
        for artist in self.annotation_artists:
            artist.set_visible(False)
        for artist in self.footer_artists:
            artist.set_visible(False)

    def show_footer(self):
        for artist in self.footer_artists:
            #  inspect(artist)
            artist.set_visible(True)

    def hide_footer(self):
        for artist in self.footer_artists:
            artist.set_visible(False)

    def highlight(self):
        # Highlight the main artifact (you might want to change the color, style or other properties)
        pass

    def select(self):
        # Select the main artifact and related elements
        for artist in self.selected_artists:
            artist.set_visible(True)

    def dim(self):
        # Dim the main artifact (you might want to reduce opacity or change other visual properties)
        # TODO: determine how to set opacity
        pass

    def annotate(self):
        # Annotate the main artifact with the provided annotation
        for artist in self.annotation_artists:
            artist.set_visible(True)

    def set_label(self, label):
        # Set label for the main artifact
        self.label = label

    def set_description(self, description):
        # Set description for the main artifact
        self.description = description

    def set_zoom_pts(self, points):
        # Set zoom points for the main artifact
        self.zoom_pts = points


def _plot_element(self, index, el, model):
    """
    instanstiates and returns a PlotElement object
    containing all the necessary matplotlib artifacts for rendering a geometric element
    """

    details = model[el]

    #  zoom_pts = []
    annotate_points = []

    plot_element = PlotElement(None)

    if isinstance(el, spg.Point):
        typ = "point"
        description = (
            f"$\\left\{{ \\ {sp.latex(el.x)}, \\ {sp.latex(el.y)} \\ \\right\}}$"
        )

        #  pt_inner, *pts = self.plot_point(el, details.classes)
        plot_element.main_artists.extend(self.plot_point(el, details.classes))

        annotate_points.append(el)
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

        plot_element.zoom_pts.append(el)

        if "given" not in details.classes:
            for parent in list(details.parents.keys())[0:2]:
                if isinstance(parent, spg.Line):
                    parent_classes = model[parent].classes
                    plot_element.selected_artists.extend(
                        self.plot_selected_line(parent, parent_classes)
                    )
                if isinstance(parent, spg.Circle):
                    parent_classes = model[parent].classes
                    plot_element.selected_artists.extend(
                        self.plot_selected_circle(
                            parent,
                            parent_classes,
                        )
                    )
        plot_element.selected_artists.extend(self.plot_selected_points([el]))

    if isinstance(el, spg.Line):
        typ = "line"
        eq = el.equation().simplify()
        dist = sp.sqrtdenest(el.p1.distance(el.p2).simplify())
        description = f"${sp.latex(eq)} = 0$ \n $d = {sp.latex(dist)}$"

        plot_element.main_artists.extend(self.plot_line(el, details.classes))

        plot_element.zoom_pts.extend(el.points)

        plot_element.selected_artists.extend(
            self.plot_selected_line(el, details.classes)
        )
        plot_element.selected_artists.extend(
            self.plot_line_segment(el, details.classes)
        )
        plot_element.selected_artists.extend(self.plot_selected_points(el.points))

        annotate_points.extend(el.points)
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

    if isinstance(el, spg.Circle):
        typ = "circle"
        eq = el.equation().simplify()
        rad = sp.sqrtdenest(el.radius.simplify())
        area = sp.sqrtdenest(el.area.simplify())
        areaf = str(round(float(area.evalf()), 4))
        description = f"${sp.latex(eq)} = 0$ \n $r = {sp.latex(rad)}$"

        plot_element.main_artists.extend(self.plot_circle(el, details.classes))

        annotate_points.extend([el.center, details.pt_radius])
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

        p1_x, p1_y, p2_x, p2_y = el.bounds
        p1 = spg.Point(p1_x, p1_y)
        p2 = spg.Point(p2_x, p2_y)
        plot_element.zoom_pts.append(p1)
        plot_element.zoom_pts.append(p2)

        radius_segment = spg.Segment(el.center, details.pt_radius)
        plot_element.selected_artists.extend(
            self.plot_circle_radius(
                radius_segment,
                details.classes,
            )
        )
        plot_element.selected_artists.extend(
            self.plot_selected_circle(
                el,
                details.classes,
            )
        )
        plot_element.selected_artists.extend(
            self.plot_circle_points([el.center, details.pt_radius])
        )

    if isinstance(el, spg.Segment):
        typ = "segment"
        seg = sp.sqrtdenest(el.length.simplify())
        segf = str(round(float(seg.evalf()), 4))
        description = f"seg: ${sp.latex(seg)}$"
        description += " $ \\approx " + segf + "$"

        plot_element.main_artists.extend(self.plot_segment(el, details.classes))

        annotate_points.extend(el.points)
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

        plot_element.zoom_pts.extend(el.points)
        plot_element.selected_artists.extend(self.plot_selected_points(el.points))

    if isinstance(el, spg.Polygon):
        typ = "polygon"
        area = sp.sqrtdenest(el.area.simplify())
        areaf = str(round(float(area.evalf()), 4))
        perim = sp.sqrtdenest(el.perimeter.simplify())
        perimf = str(round(float(perim.evalf()), 4))
        description = f"area: ${sp.latex(area)} \\approx {areaf}$ "
        description += "\n"
        description += f"perim: ${sp.latex(perim)} \\approx {perimf}$"

        plot_element.main_artists.extend(self.plot_polygon([el], details.classes))

        annotate_points.extend(el.vertices)
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

        # TODO: refactor plot_polygons
        plot_element.zoom_pts.extend(el.vertices)
        plot_element.selected_artists.extend(self.plot_selected_points(el.vertices))

    if isinstance(el, Wedge):
        typ = "wedge"
        area = sp.sqrtdenest(el.area.simplify())
        areaf = str(round(float(area.evalf()), 4))
        perim = sp.sqrtdenest(el.perimeter.simplify())
        perimf = str(round(float(perim.evalf()), 4))
        description = f"area: ${sp.latex(area)} \\approx {areaf}$ "
        # TODO: determine why radians create and error
        #  description += "\n"
        #  description += f"rad: ${sp.latex(el.radians)} \n deg: {sp.latex(el.degrees)}$"

        plot_element.main_artists.extend(self.plot_wedge(el, details.classes))

        annotate_points.extend(
            [el.pt_center, el.pt_radius, el.start_point, el.end_point]
        )
        for pt in annotate_points:
            label = model[pt].label
            plot_element.annotation_artists.extend(self.annotate_point(pt, label))

        plot_element.zoom_pts.extend(el.points)

        plot_element.selected_artists.extend(self.plot_selected_points(el.points))

    plot_element.footer_artists.extend(
        self.plot_footer(f"{index:03}", description, details.label)
    )


    # TODO: selected set by caller
    #  self.selected = selected

    # TODO: draw should be done by the caller
    #  plt.draw()

    return plot_element

```

## src/geometor/render/plotter/_lines.py

```py
"""
method implementations for the ``Plotter`` class

- _plot_line
- _plot_selected_line

"""
# permits forward reference for Plotter class
from __future__ import annotations

from ..common import *
from ..styles import *


def _plot_line(
    plotter: Plotter,
    line: spg.Line,
    classes: list = None,
) -> list[mp.Line2D]:
    """
    returns list of plot artists
    """
    if classes is None:
        classes = []

    ends = plotter.bounds.intersection(line)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = get_styles("line", classes)
    return plotter.ax_main.plot(xs, ys, **styles)


def _plot_selected_line(
    plotter: Plotter,
    line: spg.Line,
    classes: list = None,
) -> list[mp.Line2D]:
    """
    returns list of plot artists
    """
    if classes is None:
        classes = []

    ends = plotter.bounds.intersection(line)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = get_styles("line", classes)
    styles.update(get_styles("line_selected", classes))
    return plotter.ax_main.plot(xs, ys, **styles)



```

## src/geometor/render/plotter/_points.py

```py
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

```

## src/geometor/render/plotter/_polygons.py

```py
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





```

## src/geometor/render/plotter/_segments.py

```py
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

```

## src/geometor/render/plotter/_wedges.py

```py
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





```

## src/geometor/render/ranges.py

```py
"""
functions to plot ranges

a range would be 4 or more points on line in a harmonic proportion
"""

from .common import *
from .styles import *
from .utils import *
from .points import *
from .segments import *
from .groups import *


def plot_harmonics_by_segment(
    NAME, ax, ax_label, model, harmonics_by_segment, png=False
):
    #  sorted_groups_keys = sorted(groups.keys(), key=lambda key: float(key.evalf()), reverse=True)
    for i, (line, groups) in enumerate(harmonics_by_segment.items()):
        for j, (segment, group) in enumerate(groups.items()):
            filename = f"{i:03}-{j:05}"

            #  groupf = str(float(group.evalf()))[0:6]
            #  title=f'${sp.latex(group)} \\ \\approx {groupf}\\ldots$'
            title = filename
            plot_group_sections(
                NAME,
                ax,
                ax_label,
                model,
                group,
                filename=filename,
                title=title,
                folder="harmonics",
                png=png,
            )


def plot_all_ranges(NAME, ax, ax_btm, history, ranges, bounds):
    xlabel = f"ranges: {len(ranges)}"
    ax_prep(ax, ax_btm, bounds, xlabel)
    for i, rng in enumerate(ranges):
        gold_points(ax, rng)
        seg = segment(rng[0], rng[3])
        plot_segment2(ax, seg)

    plot_sequence(ax, history, bounds)
    snapshot(f"{NAME}/ranges", f"summary.png")


def plot_ranges(NAME, ax, ax_btm, history, ranges, bounds):
    """plot each range from points"""
    for i, rng in enumerate(ranges):
        ad = segment(rng[0], rng[3]).length.simplify()
        cd = segment(rng[2], rng[3]).length.simplify()
        ac = segment(rng[0], rng[2]).length.simplify()
        bc = segment(rng[1], rng[2]).length.simplify()
        #  return sp.simplify((ad / cd) - (ac / bc))
        ratio1 = str(float((ad / cd).evalf()))[0:6]
        ratio2 = str(float((ac / bc).evalf()))[0:6]

        num = str(i).zfill(5)
        xlabel = num
        # escape outer brackers for \frac
        xlabel = f"${ratio1}\\ldots \\approx \\ \\frac {{ {sp.latex(ad)} }} {{{sp.latex(cd)} }}$"
        xlabel += f"  :  "
        xlabel += f"$ \\frac {{ {sp.latex(ac)} }} {{{sp.latex(bc)} }} \\ \\approx {ratio2}\\ldots$"
        ax_prep(ax, ax_btm, bounds, xlabel)
        #  print(i, rng)
        gold_points(ax, rng)
        seg = segment(rng[0], rng[3])
        plot_segment2(ax, seg)
        plot_sequence(ax, history, bounds)
        snapshot(f"{NAME}/ranges", f"{num}.png")

        # zoom around section points
        limx, limy = get_limits_from_points(rng, margin=0.5)
        limx, limy = adjust_lims(limx, limy)
        ax.set_xlim(limx[0], limx[1])
        ax.set_ylim(limy[0], limy[1])

        snapshot(f"{NAME}/ranges", f"{num}-zoom.png")

```

## src/geometor/render/sections.py

```py
"""
functions to plot sections identified in the model

a section is defined as three point along a line
"""

from .common import *
from geometor.model import *
from geometor.render import *


def _get_points_from_sections(sections):
    section_pts = {}
    for i, section in enumerate(sections):
        for pt in section.points:
            section_pts[pt] = ""
    return list(section_pts)



def plot_section(
    plotter: Plotter, model: Model, index, section, extensions=["svg", "png"]
):
    """
    plot the section then remove it
    """
    files = []

    l1, l2 = section.lengths
    f1, f2 = section.floats
    description = r"\begin{align*}"
    description += f"{sp.latex(l1)} \\ &: \\ {sp.latex(l2)}\\\\"
    description += f"{f1:.6f}\\ldots \\ &: \\ {f2:.6f}\\ldots"
    description += r"\end{align*}"

    section_pts = section.points

    selected = []

    selected.append(plotter.plot_selected_points(section_pts))
    for seg in section.segments:
        selected.append(plotter.plot_segment(seg))

    label = "_".join(section.get_labels(model))

    plotter.plot_footer(index, description, label)

    folder = f"./{plotter.plot_name}/sections"
    filename = f"{index:05}"

    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}.{ext}"))

    # annotate points
    for pt in section_pts:
        label = model[pt].label
        selected.append(plotter.annotate_point(pt, label))

    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}-label.{ext}"))

    # zoom around section points
    x_limits, y_limits = get_limits_from_points(section_pts)
    x_limits, y_limits = plotter._add_margin_to_ax_main_limits(x_limits, y_limits)
    x_limits, y_limits = plotter._pad_ax_main_limits_for_aspect_ratio(
        x_limits, y_limits
    )

    plotter.ax_main.set_xlim(x_limits[0], x_limits[1])
    plotter.ax_main.set_ylim(y_limits[0], y_limits[1])

    for ext in extensions:
        files.append(snapshot_2(folder, f"{filename}-zoom.{ext}"))

    for select in selected:
        #  print(f"{select=}")
        #  breakpoint()
        selected_el = select.pop(0)
        selected_el.remove()

    # reset view after zoom
    plotter.set_ax_main_bounds(plotter.bounds)

    return files


def plot_sections(
    plotter: Plotter, model: Model, sections: list, extensions=["svg", "png"]
):
    sections_pts = _get_points_from_sections(sections)
    plotter.set_plotter_limits_from_points(sections_pts)

    files = []

    for index, section in enumerate(sections):
        files.extend(plot_section(plotter, model, index, section))

    return files

def plot_all_sections(
    plotter: Plotter, model: Model, sections: list, extensions=["svg", "png"]
):
    sections_pts = _get_points_from_sections(sections)
    plotter.set_plotter_limits_from_points(sections_pts)

    files = []

    for index, section in enumerate(sections):
        for segment in section.segments:
            plotter.plot_segment(segment)

    folder = f"./{plotter.plot_name}/sections"
    for ext in extensions:
        files.append(snapshot_2(folder, f"all.{ext}"))
    return files


```

## src/geometor/render/sequencer/_animate.py

```py
"""
functions to plot models as a sequential build
"""

from __future__ import annotations

from ..common import *
from ..styles import *
from ..utils import *
from matplotlib.animation import FuncAnimation

from .._html import _create_html_page

from geometor.model import Wedge


def _animate_sequence(self, model: Model, extensions=["svg", "png"]):
    """\
    Plots the sequence of all types of elements in layers for the given model.
    """
    x_limits, y_limits = model.limits()
    x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
    x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(x_limits, y_limits)

    self.bounds = spg.Polygon(
        spg.Point(x_limits[0], y_limits[1]),
        spg.Point(x_limits[0], y_limits[0]),
        spg.Point(x_limits[1], y_limits[0]),
        spg.Point(x_limits[1], y_limits[1]),
    )
    self.set_ax_main_bounds(self.bounds)

    cursor_points = []

    def init():
        # Initialization function: plot the background of each frame
        return (self.fig,)

    def update(frame):
        el = list(model.keys())[frame]
        details = model[el]
        i = frame

        selected = []
        zoom_pts = []
        annotate_points = []

        if isinstance(el, spg.Point):
            typ = "point"
            label = (
                f"$\\left\{{ \\ {sp.latex(el.x)}, \\ {sp.latex(el.y)} \\ \\right\}}$"
            )

            pt_inner, *pts = self.plot_point(el, details.classes, add_to_cursors=False)
            cursor_points.append(pt_inner.pop())
            annotate_points.append(el)
            zoom_pts.append(el)
            if "given" not in details.classes:
                for parent in list(details.parents.keys())[0:2]:
                    if isinstance(parent, spg.Line):
                        selected.append(self.plot_selected_line(parent, []))
                    if isinstance(parent, spg.Circle):
                        selected.append(
                            self.plot_selected_circle(
                                parent,
                                [],
                            )
                        )
            selected.append(self.plot_selected_points([el]))

        if isinstance(el, spg.Line):
            typ = "line"
            eq = el.equation().simplify()
            dist = sp.sqrtdenest(el.p1.distance(el.p2).simplify())
            label = f"${sp.latex(eq)} = 0$ \n $d = {sp.latex(dist)}$"
            annotate_points.extend(el.points)

            self.plot_line(el, details.classes)

            zoom_pts.extend(el.points)

            selected.append(self.plot_selected_line(el, details.classes))
            selected.append(self.plot_line_segment(el, details.classes))
            selected.append(self.plot_selected_points(el.points))

        if isinstance(el, spg.Circle):
            typ = "circle"
            eq = el.equation().simplify()
            rad = sp.sqrtdenest(el.radius.simplify())
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            annotate_points.extend([el.center, details.pt_radius])

            label = f"${sp.latex(eq)} = 0$ \n $r = {sp.latex(rad)}$"

            self.plot_circle(el, details.classes)

            zoom_pts.extend(el.bounds)

            selected.append(
                self.plot_circle_radius(
                    el.center,
                    details.pt_radius,
                    details.classes,
                )
            )
            selected.append(
                self.plot_selected_circle(
                    el,
                    details.classes,
                )
            )
            selected.append(self.plot_circle_points([el.center, details.pt_radius]))

        if isinstance(el, spg.Segment):
            typ = "segment"
            seg = sp.sqrtdenest(el.length.simplify())
            segf = str(round(float(seg.evalf()), 4))
            annotate_points.extend(el.points)

            label = f"seg: ${sp.latex(seg)}$"
            label += " $ \\approx " + segf + "$"

            self.plot_segment(el, details.classes)
            zoom_pts.extend(el.points)
            selected.append(self.plot_selected_points(el.points))

        if isinstance(el, spg.Polygon):
            typ = "polygon"
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))
            annotate_points.extend(el.vertices)

            label = f"area: ${sp.latex(area)} \\approx {areaf}$ "
            label += "\n"
            label += f"perim: ${sp.latex(perim)} \\approx {perimf}$"

            # TODO: refactor plot_polygons
            self.plot_polygon([el], details.classes)
            zoom_pts.extend(el.vertices)
            selected.append(self.plot_selected_points(el.vertices))

        if isinstance(el, Wedge):
            typ = "wedge"
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))
            annotate_points.extend(
                [el.pt_center, el.pt_radius, el.start_point, el.end_point]
            )

            label = f"area: ${sp.latex(area)} \\approx {areaf}$ "
            label += "\n"
            label += f"rad: ${sp.latex(el.radians)} \n deg: {sp.latex(el.degrees)}$"

            # TODO: refactor plot_polygons
            self.plot_wedge(el, details.classes)
            #  zoom_pts.extend(el.vertices)
            #  selected.append(self.plot_selected_points(el.vertices))

        # add classes to type name
        if details.classes:
            typ += "-"
            typ += "_".join(details.classes)

        self.plot_footer(f"{i:03}", label, details.label)

        steps_folder = f"./{self.plot_name}/steps"
        filename = f"{i:05}-{typ}"

        #  for ext in extensions:
        #  files[ext].append(snapshot_2(steps_folder, f"{filename}.{ext}"))

        # annotate points
        for pt in annotate_points:
            label = model[pt].label
            selected.append(self.annotate_point(pt, label))

        #  for ext in extensions:
        #  files[ext].append(snapshot_2(steps_folder, f"{filename}-label.{ext}"))

        #  # zoom around section points
        #  limx, limy = get_limits_from_points(section_pts, margin=.5)
        #  limx, limy = adjust_lims(limx, limy)

        #  ax.set_xlim(limx[0], limx[1])
        #  ax.set_ylim(limy[0], limy[1])

        #  #  snapshot(f'{NAME}/sections', f'{num}-zoom.png')
        #  snapshot_2(f'./{self.plot_name}/steps', f'{filename}-zoom.png')
        #  snapshot_2(f'./{self.plot_name}/steps', f'{filename}-zoom.svg')

        for select in selected:
            selected_el = select.pop(0)
            selected_el.remove()

    label = f"elements: {len(model)} • points: {len(model.points)}"
    self.plot_footer("", label, "")

    #  for ext in extensions:
    #  files[ext].append(snapshot_2(steps_folder, f"summary.{ext}"))

    mplcursors.cursor(cursor_points, highlight=True)

    #  _create_html_page(files['svg'], output_path=f"{self.plot_name}.html")
    anim = FuncAnimation(
        self.fig, update, init_func=init, frames=len(model.items()), blit=True
    )

    #  plt.show()
    anim.save(f'{model.name}.mp4', writer='ffmpeg')

```

## src/geometor/render/sequencer/_plot.py

```py
"""
functions to plot models as a sequential build
"""

from __future__ import annotations

from ..common import *
from ..styles import *
from ..utils import *
from matplotlib.animation import FuncAnimation

from .._html import _create_html_page

from geometor.model import Wedge

#  from geometor.render.sequencer.sequencer import Sequencer


def _plot_sequence(self, model: Model, extensions=["svg", "png"]):
    """
    Plots the sequence of all types of elements in layers for the given model.
    """
    x_limits, y_limits = model.limits()
    x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
    x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(x_limits, y_limits)

    self.bounds = spg.Polygon(
        spg.Point(x_limits[0], y_limits[1]),
        spg.Point(x_limits[0], y_limits[0]),
        spg.Point(x_limits[1], y_limits[0]),
        spg.Point(x_limits[1], y_limits[1]),
    )
    self.set_ax_main_bounds(self.bounds)

    cursor_points = []
    files = {}
    for ext in extensions:
        files[ext] = []

    for i, (el, details) in enumerate(model.items()):
        selected = []
        zoom_pts = []
        annotate_points = []

        if isinstance(el, spg.Point):
            typ = "point"
            label = (
                f"$\\left\{{ \\ {sp.latex(el.x)}, \\ {sp.latex(el.y)} \\ \\right\}}$"
            )

            pt_inner, *pts = self.plot_point(el, details.classes, add_to_cursors=False)
            cursor_points.append(pt_inner.pop())
            annotate_points.append(el)
            zoom_pts.append(el)
            if "given" not in details.classes:
                for parent in list(details.parents.keys())[0:2]:
                    if isinstance(parent, spg.Line):
                        selected.append(self.plot_selected_line(parent, []))
                    if isinstance(parent, spg.Circle):
                        selected.append(
                            self.plot_selected_circle(
                                parent,
                                [],
                            )
                        )
            selected.append(self.plot_selected_points([el]))

        if isinstance(el, spg.Line):
            typ = "line"
            eq = el.equation().simplify()
            dist = sp.sqrtdenest(el.p1.distance(el.p2).simplify())
            label = f"${sp.latex(eq)} = 0$ \n $d = {sp.latex(dist)}$"
            annotate_points.extend(el.points)

            self.plot_line(el, details.classes)

            zoom_pts.extend(el.points)

            selected.append(self.plot_selected_line(el, details.classes))
            selected.append(self.plot_line_segment(el, details.classes))
            selected.append(self.plot_selected_points(el.points))

        if isinstance(el, spg.Circle):
            typ = "circle"
            eq = el.equation().simplify()
            rad = sp.sqrtdenest(el.radius.simplify())
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            annotate_points.extend([el.center, details.pt_radius])

            label = f"${sp.latex(eq)} = 0$ \n $r = {sp.latex(rad)}$"

            self.plot_circle(el, details.classes)

            p1_x, p1_y, p2_x, p2_y = el.bounds
            p1 = spg.Point(p1_x, p1_y)
            p2 = spg.Point(p2_x, p2_y)
            zoom_pts.append(p1)
            zoom_pts.append(p2)

            selected.append(
                self.plot_circle_radius(
                    el.center,
                    details.pt_radius,
                    details.classes,
                )
            )
            selected.append(
                self.plot_selected_circle(
                    el,
                    details.classes,
                )
            )
            selected.append(self.plot_circle_points([el.center, details.pt_radius]))

        if isinstance(el, spg.Segment):
            typ = "segment"
            seg = sp.sqrtdenest(el.length.simplify())
            segf = str(round(float(seg.evalf()), 4))
            annotate_points.extend(el.points)

            label = f"seg: ${sp.latex(seg)}$"
            label += " $ \\approx " + segf + "$"

            self.plot_segment(el, details.classes)
            zoom_pts.extend(el.points)
            selected.append(self.plot_selected_points(el.points))

        if isinstance(el, spg.Polygon):
            typ = "polygon"
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))
            annotate_points.extend(el.vertices)

            label = f"area: ${sp.latex(area)} \\approx {areaf}$ "
            label += "\n"
            label += f"perim: ${sp.latex(perim)} \\approx {perimf}$"

            # TODO: refactor plot_polygons
            self.plot_polygon([el], details.classes)
            zoom_pts.extend(el.vertices)
            selected.append(self.plot_selected_points(el.vertices))

        if isinstance(el, Wedge):
            typ = "wedge"
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))
            annotate_points.extend(
                [el.pt_center, el.pt_radius, el.start_point, el.end_point]
            )

            label = f"area: ${sp.latex(area)} \\approx {areaf}$ "
            label += "\n"
            label += f"rad: ${sp.latex(el.radians)} \n deg: {sp.latex(el.degrees)}$"

            # TODO: refactor plot_polygons
            self.plot_wedge(el, details.classes)
            #  zoom_pts.extend(el.vertices)
            #  selected.append(self.plot_selected_points(el.vertices))

        # add classes to type name
        if details.classes:
            typ += "-"
            typ += "_".join(details.classes)

        self.plot_footer(f"{i:03}", label, details.label)

        steps_folder = f"./{self.plot_name}/steps"
        filename = f"{i:05}-{typ}"

        for ext in extensions:
            files[ext].append(snapshot_2(steps_folder, f"{filename}.{ext}"))

        # annotate points
        for pt in annotate_points:
            label = model[pt].label
            selected.append(self.annotate_point(pt, label))

        for ext in extensions:
            files[ext].append(snapshot_2(steps_folder, f"{filename}-label.{ext}"))

        # set zoom
        if zoom_pts:
            x_limits, y_limits = get_limits_from_points(zoom_pts)
            x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
            x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(
                x_limits, y_limits
            )

            self.ax_main.set_xlim(x_limits[0], x_limits[1])
            self.ax_main.set_ylim(y_limits[0], y_limits[1])

            for ext in extensions:
                files[ext].append(snapshot_2(steps_folder, f"{filename}-zoom.{ext}"))

        # undo zoom
        self.set_ax_main_bounds(self.bounds)

        for select in selected:
            selected_el = select.pop(0)
            selected_el.remove()

    label = f"elements: {len(model)} • points: {len(model.points)}"
    self.plot_footer("", label, "")

    for ext in extensions:
        files[ext].append(snapshot_2(steps_folder, f"summary.{ext}"))

    mplcursors.cursor(cursor_points, highlight=True)

    #  _create_html_page(files['svg'], output_path=f"{self.plot_name}.html")

```

## src/geometor/render/sequencer/_step.py

```py
"""
functions to step through model
"""
from __future__ import annotations

from ..common import *
from ..styles import *
from ..utils import *
from matplotlib.widgets import Button, CheckButtons
import matplotlib.animation as animation

from geometor.model import Wedge


class UIElements:
    def __init__(self, plotter_context):
        self.plotter_context = plotter_context
        self.buttons = {}  # Add this line to store button references
        self.buttons['start'] = self.create_button(0, "start", self._go_to_start)
        self.buttons['prev'] = self.create_button(0.1, "prev", self._step_back)
        self.buttons['next'] = self.create_button(0.2, "next", self._step_forward)
        self.buttons['end'] = self.create_button(0.3, "end", self._go_to_end)
        self.buttons['play'] = self.create_button(0.4, "play", self._on_play)
        self.buttons['pause'] = self.create_button(0.5, "pause", self._on_pause)
        # Connect the key press event to the function
        plt.connect("key_press_event", self.on_key)

    def init_func(self):
        """Initial function to setup the animation"""
        for element in self.plotter_context.plot_elements:
            element.hide()
        plt.draw()

    def _on_play(self, event):
        self.ani = animation.FuncAnimation(
            plt.gcf(),
            self.update,
            init_func=self.init_func,
            frames=len(self.plotter_context.plot_elements),
            repeat=False,
            interval=1000,
        )
        self.ani.event_source.start()  # Start the animation when the play button is pressed

    def _on_pause(self, event):
        self.ani.event_source.stop()
    
    def on_key(self, event):
        # Check for specific key presses and call the corresponding functions
        if event.key in ["right", "j"]:
            self._step_forward(None)
        elif event.key in ["left", "k"]:
            self._step_back(None)
        elif event.key in ["up", "h"]:
            self._go_to_start(None)
        elif event.key in ["down", "l"]:
            self._go_to_end(None)
        elif event.key in [" "]:
            self._on_play(None)
        elif event.key in ["p"]:
            self._on_pause(None)

    def update(self, frame):
        if frame < len(self.plotter_context.plot_elements):
            for i, element in enumerate(self.plotter_context.plot_elements):
                if i < frame:
                    element.hide()
                    element.show()
                elif i <= frame:
                    element.show()
                    element.select()
                    element.annotate()
                    element.show_footer()
                else:
                    element.hide()

            plt.draw()


    def create_button(
        self, offset, label, on_click, color="lightgray", hovercolor="gray"
    ):
        ax = plt.axes([offset, 0.92, 0.09, 0.05])
        button = Button(ax, label, color=color, hovercolor=hovercolor)
        button.label.set_fontsize(10)
        button.label.set_color("black")  # To change the text color
        button.on_clicked(on_click)
        return button

    def create_check_buttons(self, ax, labels, states, on_click):
        rax = plt.axes([0.55, 0.92, 0.15, 0.05])
        check = CheckButtons(rax, ("Zoom", "Labels"), (False, False))
        check.on_clicked(_toggle_buttons)

    def _go_to_start(self, event):
        plotter = self.plotter_context
        plotter.current_index = 0
        for i, element in enumerate(plotter.plot_elements):
            if i == 0:
                element.show()
                element.select()
                element.annotate()
                element.show_footer()
            else:
                element.hide()
        plt.draw()

    def _go_to_end(self, event):
        plotter = self.plotter_context
        plotter.current_index = len(plotter.plot_elements) - 1
        for i, element in enumerate(plotter.plot_elements):
            if i < plotter.current_index:
                element.hide()
                element.show()
            elif i == plotter.current_index:
                element.show()
                element.select()
                element.annotate()
                element.show_footer()
            else:
                element.hide()
        plt.draw()

    def _step_back(self, event):
        plotter = self.plotter_context
        if plotter.current_index > 0:
            plotter.current_index -= 1
            for i, element in enumerate(plotter.plot_elements):
                if i < plotter.current_index:
                    element.hide()
                    element.show()
                elif i == plotter.current_index:
                    element.show()
                    element.select()
                    element.annotate()
                    element.show_footer()
                else:
                    element.hide()

            plt.draw()

    def _step_forward(self, event):
        plotter = self.plotter_context
        if plotter.current_index < len(plotter.plot_elements) - 1:
            plotter.current_index += 1
            for i, element in enumerate(plotter.plot_elements):
                if i < plotter.current_index:
                    element.hide()
                    element.show()
                elif i == plotter.current_index:
                    element.show()
                    element.select()
                    element.annotate()
                    element.show_footer()
                else:
                    element.hide()

            plt.draw()

    def _toggle_buttons(label):
        if label == "Zoom":
            _toggle_zoom()
        elif label == "Labels":
            _toggle_labels()

    def _toggle_zoom():
        # Your code to toggle zoom
        pass

    def _toggle_labels():
        # Your code to toggle labels
        pass


def _step_sequence(self, model: Model):
    """
    allow interactive stepping through the model
    """
    print("\nstep sequence: ", model.name)
    ui = UIElements(self)

    # set up model
    # TODO: this should be one method on plotter
    x_limits, y_limits = model.limits()
    x_limits, y_limits = self._add_margin_to_ax_main_limits(x_limits, y_limits)
    x_limits, y_limits = self._pad_ax_main_limits_for_aspect_ratio(x_limits, y_limits)

    self.bounds = spg.Polygon(
        spg.Point(x_limits[0], y_limits[1]),
        spg.Point(x_limits[0], y_limits[0]),
        spg.Point(x_limits[1], y_limits[0]),
        spg.Point(x_limits[1], y_limits[1]),
    )
    self.set_ax_main_bounds(self.bounds)

    # TODO: reintegrate cursor points
    cursor_points = []

    for index, el in enumerate(model):
        print(index, el)
        plot_element = self.plot_element(index, el, model)
        plot_element.hide()
        self.plot_elements.append(plot_element)

    self.current_index = 0
    self.plot_elements[0].show()
    self.plot_elements[0].select()
    self.plot_elements[0].annotate()
    self.plot_elements[0].show_footer()

    mplcursors.cursor(cursor_points, highlight=True)

    plt.show()

```

## src/geometor/render/styles/_blue.py

```py
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

```

## src/geometor/render/styles/_default.py

```py
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

```

## src/geometor/render/styles/_green.py

```py
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

```

## src/geometor/render/styles/_red.py

```py
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

```

## src/geometor/render/styles/z_levels.py

```py

Z_LINE = 10
Z_CIRCLE = 11
Z_SEGMENT = 12
Z_POLYGON = 13
Z_SELECTED = 40
Z_POINT_HILITE = 50  #hilite under everything
Z_POINT_OUTER = 51  #dark ring
Z_POINT_INNER = 52  #light dot

```

## src/geometor/render/utils.py

```py
"""
functions to plot utils
"""

from .common import *


def set_bounds(limx, limy) -> sp.Polygon:
    return sp.Polygon(
        spg.Point(limx[0], limy[1]),
        spg.Point(limx[0], limy[0]),
        spg.Point(limx[1], limy[0]),
        spg.Point(limx[1], limy[1])
        )


def snapshot(folder, filename):
    import os
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{folder}/'
    os.makedirs(out, exist_ok=True)
    filename = out + filename
    plt.savefig(filename, dpi=120)
    print_log(f'    * {filename}')
    return filename


def snapshot_2(folder, filename, transparent=False):
    import os
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, filename)
    plt.savefig(filename, dpi=120, transparent=transparent)
    print_log(f'    * {filename}')
    return filename


def display(filename):
    from IPython import display
    display.Image(filename)


#  def ax_prep(ax, ax_btm, bounds, xlabel):
    #  ax.clear()
    #  ax_btm.clear()
    #  ax.axis(False)
    #  ax_btm.axis(False)
    #  #  ax.spines['bottom'].set_color('k')
    #  #  ax.spines['top'].set_color('k')
    #  #  ax.spines['right'].set_color('k')
    #  #  ax.spines['left'].set_color('k')
    #  #  ax.tick_params(axis='x', colors='k')
    #  #  ax.tick_params(axis='y', colors='k')
    #  vmin = bounds.vertices[0]
    #  vmax = bounds.vertices[2]
    #  ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    #  ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
    #  ax.invert_yaxis()

    #  #  ax.set_xlabel(xlabel, fontdict={'color': 'w', 'size':'20'})
    #  ax_btm.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})


def adjust_ratio(w, h, ratio):
    # TODO: account for header and footer
    if w / h < ratio:
        w = ratio * h
    if w / h > ratio:
        h = w / ratio
    return w, h

def adjust_lims(limx, limy, margin_ratio=0.1):
    # TODO: adjust ratio for header footer
    w = abs(limx[1] - limx[0])
    w_margin = w * margin_ratio
    limx[0] -= w_margin
    limx[1] += w_margin
    w = abs(limx[1] - limx[0])

    h = abs(limy[1] - limy[0])
    h_margin = h * margin_ratio
    limy[0] -= h_margin
    limy[1] += h_margin
    h = abs(limy[1] - limy[0])

    #  w2, h2 = adjust_ratio(w, h)
    w2, h2 = (w, h)
    xdiff = abs(w2 - w) / 2
    ydiff = abs(h2 - h) / 2

    limx[0] -= xdiff
    limx[1] += xdiff
    limy[0] -= ydiff
    limy[1] += ydiff

    return limx, limy


def get_limits_from_points(pts):
    '''find x, y limits from a set of points'''
    limx = [0, 0]
    limy = [0, 0]
    if pts:
        pt = list(pts)[0]
        ptx = float(pt.x.evalf())
        pty = float(pt.y.evalf())
        limx[0] = ptx
        limx[1] = ptx
        limy[0] = pty
        limy[1] = pty

        for pt in pts:
            ptx = float(pt.x.evalf())
            pty = float(pt.y.evalf())
            # print(x, y)
            limx[0] = ptx if ptx < limx[0] else limx[0]
            limx[1] = ptx if ptx > limx[1] else limx[1]
            limy[0] = pty if pty < limy[0] else limy[0]
            limy[1] = pty if pty > limy[1] else limy[1]

    return limx, limy



####
# more generalized plot setup
def ax_set_bounds(ax, bounds):
    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))

def ax_set_spines(ax):
    ax.spines['bottom'].set_color('k')
    ax.spines['top'].set_color('k')
    ax.spines['right'].set_color('k')
    ax.spines['left'].set_color('k')
    ax.tick_params(axis='x', colors='k')
    ax.tick_params(axis='y', colors='k')


```

