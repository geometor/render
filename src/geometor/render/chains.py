
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

