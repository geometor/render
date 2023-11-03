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
