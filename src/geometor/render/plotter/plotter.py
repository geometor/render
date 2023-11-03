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

    parameters:
        ``name`` : :class:`str`
            establish name for the model instance

    attributes:
        :attr:`plot_name` : :class:`str`
            name of the model
        :attr:`margin` : :class:`float`
            margin for the plot
        :attr:`FIG_W` : :class:`int`
            width of the figure
        :attr:`FIG_H` : :class:`int`
            height of the figure
        :attr:`ax_main` : :class:`matplotlib.axes.Axes`
            Axes for the main graph
        :attr:`ax_header` : :class:`matplotlib.axes.Axes`
            Axes for the header panel
        :attr:`ax_footer` : :class:`matplotlib.axes.Axes`
            Axes for the footer panel
        :attr:`figure` : :class:`matplotlib.figure.Figure`
            the main figure of the plot

    methods:
        :meth:`plot_point` : :class:`Point <sympy.geometry.point.Point>`
            - plot from sympy point
        :meth:`plot_line` : :class:`Line <sympy.geometry.line.Line>`
            - plot from sympy line
        :meth:`plot_circle` : :class:`Circle <sympy.geometry.ellipse.Circle>`
            - construct line from two points
            - add to model if unique
            - coordinate meta data
            - find intersections with other structs
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
                    el, details.label, details.classes, add_to_cursors=True
                )
                details.pt = el
                self.cursor_points[pt_inner.pop()] = details
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


