"""
find area of triangle within square 
https://twitter.com/dment37/status/1714728279641399629
"""
from geometor.model import *
from geometor.render import *

def run():
    model = Model('puzzle_7')
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(12, 0, classes=['given'])
    C = model.set_point(12, 12, classes=['given'])
    D = model.set_point(0, 12, classes=['given'])
    model.set_polygon([A, B, C, D])

    E = model.set_point(6, 0, classes=['given'])

    #  model.construct_line(A, B)
    model.construct_line(D, E)
    model.construct_circle(E, D)
    model.construct_circle(D, E)

    bp1 = model.points[-1]
    bp2 = model.points[-2]

    model.construct_line(bp1, bp2)

    p3 = model.points[-1]
    model.construct_circle(p3, D)
    p4 = model.points[-1]
    t1 = model.set_polygon([D, E, p4])

    #  report_summary(model)
    #  report_group_by_type(model)
    #  report_sequence(model)

    #  model.save('vesica.json')


    #  m2 = model.load("vesica.json")
    #  report_sequence(m2)
    #  print(m2)

    sequencer = Sequencer(model, FIG_W=9, FIG_H=9, margin=.01)
    sequencer.plot_sequence()

    #  ancestors = model.get_ancestors(F)
    #  print(ancestors)
    #  ancestors = model.get_ancestors_labels(F)
    #  print(ancestors)

if __name__ == '__main__':
    run()
