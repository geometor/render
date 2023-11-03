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
