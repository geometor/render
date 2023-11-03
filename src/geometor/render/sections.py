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

