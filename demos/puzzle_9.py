"""
https://twitter.com/TaghiBehradfar/status/1715021211564908928
"""
from geometor.model import *
from geometor.render import *

from geometor.model.helpers import *

def run():
    model = Model('puzzle_9')
    A = model.set_point(0, 0, classes=['given'])
    A, B, C, D = set_given_square_points(model, A, 2)
    model.set_polygon([A, B, C, D])
    B, E, F, G = set_given_square_points(model, B, 1)
    G, F, H, C = set_given_square_points(model, G, 1)

    model.construct_line(D, E)

    construct_perpendicular_bisector(model, D, E, False)

    K = model.get_element_by_label('K')

    model.construct_circle(K, D)
    model.construct_line(A, C)
    
    M = model.get_element_by_label('M')
    model.set_wedge(E, M, M, D)

    #  construct_perpendicular_bisector(model, A, D, False)
    #  model.construct_line(A, D)

    #  p1 = model.get_element_by_label('L')
    #  construct_perpendicular_bisector(model, p1, D, False)
    #  model.construct_line(B, p1)

    #  p1 = model.get_element_by_label('G')
    #  p2 = model.get_element_by_label('U')
    #  model.construct_line(p1, p2)
    #  construct_perpendicular_bisector(model, p1, p2, False)

    #  model.construct_circle_by_labels('Y', 'G')

    #  model.set_polygon_by_labels(['B', 'U', 'HH'])
    

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
