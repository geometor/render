"""
constructs the classic 'vesica pisces'
"""
from geometor.model import *
from geometor.render import *
from rich import inspect

def run():
    model = Model('vesica-2')
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(1, 0, classes=['given'])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    model.construct_circle(B, A)

    E = model.get_element_by_label('E')
    F = model.get_element_by_label('F')

    w = model.set_wedge(A, B, E, F)

    #  report_summary(model)
    #  report_group_by_type(model)
    #  report_sequence(model)

    #  model.save('vesica.json')

    #  m2 = model.load("vesica.json")

    plotter = Plotter(model.name)
    plotter.plot_model(model)
    plt.show()

    #  sequencer = Sequencer(model.name)
    #  sequencer.plot_sequence(model)

    #  titler = Titler(model, model.name)
    #  titler.plot_title("vesica pisces", ".","title.png")
    #  ancestors = model.get_ancestors(F)
    #  print(ancestors)
    #  ancestors = model.get_ancestors_labels(F)
    #  print(ancestors)

if __name__ == '__main__':
    run()
