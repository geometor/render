"""
find area of triangle within square 
https://twitter.com/dment37/status/1712541571164549618
"""
from geometor.model import *
from geometor.render import *

def run():
    model = Model('puzzle_2')
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(10, 0, classes=['given'])
    C = model.set_point(10, 10, classes=['given'])
    D = model.set_point(0, 10, classes=['given'])
    E = model.set_point(5, 10, classes=['given'])
    F = model.set_point(10, 5, classes=['given'])

    model.set_polygon([A, B, C, D])

    model.construct_line(A, E)
    model.construct_line(A, F)
    model.construct_line(E, B)

    G = model.points[-1]

    t1 = model.set_polygon([A, G, E])

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
