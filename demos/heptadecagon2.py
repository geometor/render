"""
constructs the classic 'vesica pisces'
"""
from geometor.model import *
from geometor.render import *

from geometor.model.helpers import *


def run():
    model = Model('heptadecagon')
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(1, 0, classes=['given'])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    C = model.get_element_by_label('C')

    construct_perpendicular_bisector(model, C, B, False)

    F = model.get_element_by_label('F')
    construct_perpendicular_bisector(model, A, F, False)
    
    J = model.get_element_by_label('J')
    construct_perpendicular_bisector(model, A, J, False)

    #  report_group_by_type(model)
    #  report_sequence(model)
    #  report_summary(model)

    plotter = Plotter(model)
    plotter.plot_model()

    plt.show()
    #  sequencer = Sequencer(model)
    #  sequencer.plot_sequence()

    #  plt.show()


if __name__ == '__main__':
    run()
