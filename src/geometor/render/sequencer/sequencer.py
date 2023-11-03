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

