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
