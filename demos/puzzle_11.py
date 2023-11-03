"""
https://twitter.com/TaghiBehradfar/status/1715183889268818401
"""
from geometor.model import *
from geometor.render import *

from geometor.model.helpers import *

def run():
    model = Model('puzzle_11')
    A = model.set_point(0, 0, classes=['given'])
    A, B, C, D = set_given_square_points(model, A, 2)
    model.set_polygon([A, B, C, D], classes=['red'])
    B, E, F, G = set_given_square_points(model, B, 1)
    model.set_polygon([B, E, F, G])

    model.construct_line(D, E)
    model.construct_circle(A, B)

    #  construct_perpendicular_bisector(model, D, E, False)

    #  K = model.get_element_by_label('K')

    #  model.construct_circle(K, D)
    #  model.construct_line(A, C)
    
    H = model.get_element_by_label('H')
    model.set_wedge(H, E, E, F)


    #  report_summary(model)
    #  report_group_by_type(model)
    #  report_sequence(model)

    #  model.save('vesica.json')

    #  m2 = model.load("vesica.json")
    #  report_sequence(m2)
    #  print(m2)

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
