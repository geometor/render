"""
https://twitter.com/dment37/status/1715268885555912773
"""
from geometor.model import *
from geometor.render import *

from geometor.model.helpers import *

def run():
    model = Model('puzzle_10')
    A = model.set_point(0, 0, classes=['given'])
    A, B, C, D = set_given_square_points(model, A, 1)
    B, E, F, G = set_given_square_points(model, B, 1)
    rect = model.set_polygon([A, E, F, D])

    construct_perpendicular_bisector(model, D, C, False)
    construct_perpendicular_bisector(model, C, E, False)

    K = model.get_element_by_label('K')

    model.construct_circle(K, D)
    model.construct_line(A, K)

    model.remove_by_label('L')
    model.remove_by_label('M')
    model.remove_by_label('N')
    model.remove_by_label('O')

    P = model.get_element_by_label('P')
    Q = model.get_element_by_label('Q')
    seg = model.set_segment(P, Q)

    print(seg.length * rect.area)

    #  plotter = Plotter(model, FIG_W=9, FIG_H=9, margin=.01)
    #  plotter.plot_model()

    #  plt.show()

    sequencer = Sequencer(model, FIG_W=9, FIG_H=9, margin=.01)
    sequencer.plot_sequence()

    #  ancestors = model.get_ancestors(F)
    #  print(ancestors)
    #  ancestors = model.get_ancestors_labels(F)
    #  print(ancestors)

if __name__ == '__main__':
    run()
