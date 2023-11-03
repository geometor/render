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
