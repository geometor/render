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
