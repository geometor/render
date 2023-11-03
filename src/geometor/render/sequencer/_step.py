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
