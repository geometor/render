"""
find area of triangle with square and circle
"""
from geometor.model import *
from geometor.render import *

def run():
    model = Model('puzzle_1')
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(10, 0, classes=['given'])
    C = model.set_point(10, 10, classes=['given'])
    D = model.set_point(0, 10, classes=['given'])

    model.set_polygon([A, B, C, D])

    model.construct_line(A, D)

    E = model.set_point(-2, 10, classes=['given'])

    model.construct_circle(C, E)

    F = model.get_element_by_label('F')

    t1 = model.set_polygon([A, C, F])

    report_summary(model)
    #  report_group_by_type(model)
    report_sequence(model)

    #  model.save('vesica.json')


    #  m2 = model.load("vesica.json")
    #  report_sequence(m2)
    #  print(m2)

    sequencer = Sequencer(model, FIG_W=9, FIG_H=9)
    sequencer.plot_sequence()

    #  ancestors = model.get_ancestors(F)
    #  print(ancestors)
    #  ancestors = model.get_ancestors_labels(F)
    #  print(ancestors)

if __name__ == '__main__':
    run()
