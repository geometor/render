"""
constructs the classic 'vesica pisces'
"""
from geometor.model import *
from geometor.render import *


def run():
    model = Model("puzzle_5")
    A = model.set_point(0, 0, classes=["given"])
    B = model.set_point(5, 0, classes=["given"])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    model.construct_circle(B, A)

    E = model.get_element_by_label("E")
    F = model.get_element_by_label("F")

    model.construct_line(E, A)
    model.construct_line(E, B)

    model.construct_line(F, A)
    model.construct_line(F, B)

    model.construct_circle(F, A)
    model.set_polygon_by_labels(["A", "B", "H", "K", "L", "G"])

    model.construct_line_by_labels('G', 'K')
    model.construct_line_by_labels('H', 'L')

    last_pt = model.points[-1]
    last_pt_label = model[last_pt].label
    model.set_polygon_by_labels(["A", "B", "H", last_pt_label, "G"])

    #  report_summary(model)
    #  report_group_by_type(model)
    #  report_sequence(model)

    sequencer = Sequencer(model, model.name, FIG_W=9, FIG_H=9)
    sequencer.plot_sequence()


if __name__ == "__main__":
    run()
