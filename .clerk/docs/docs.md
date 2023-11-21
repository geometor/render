


# GEOMETOR • render



## recent logs






## contents




### mission



* [goals](#goals)



Summary



#### goals







### usage




### modules




#### geometor.render


The Render Module
provides functions for plotting elements from the geometric model to
matplotlib.




##### geometor.render.plotter




*class* geometor.render.plotter.Plotter(*plot\_name: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)") | [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)") = None*, *margin\_ratio=0.1*, *FIG\_W=16*, *FIG\_H=9*)
Bases: [`object`](https://docs.python.org/3.9/library/functions.html#object "(in Python v3.9)")


The Plotter class handles the fundametals for rendering a geometric construction



###### parameters


* `name` : [`str`](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)"): establish name for the model instance




###### attributes


* `plot\_name` -> [`str`](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)"): name of the model
* `margin` -> [`float`](https://docs.python.org/3.9/library/functions.html#float "(in Python v3.9)"): margin for the plot
* `FIG\_W` -> [`int`](https://docs.python.org/3.9/library/functions.html#int "(in Python v3.9)"): width of the figure
* `FIG\_H` -> [`int`](https://docs.python.org/3.9/library/functions.html#int "(in Python v3.9)"): height of the figure
* `ax\_main` -> [`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes "(in Matplotlib v3.8.2)"): Axes for the main graph
* `ax\_header` -> [`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes "(in Matplotlib v3.8.2)"): Axes for the header panel
* `ax\_footer` -> [`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes "(in Matplotlib v3.8.2)"): Axes for the footer panel
* `figure` -> [`matplotlib.figure.Figure`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure "(in Matplotlib v3.8.2)"): the main figure of the plot




###### methods


* [`plot\_point()`](#geometor.render.plotter.Plotter.plot_point "geometor.render.plotter.Plotter.plot_point") -> [`Point`](https://docs.sympy.org/latest/modules/geometry/points.html#sympy.geometry.point.Point "(in SymPy v1.12)")
* [`plot\_line()`](#geometor.render.plotter.Plotter.plot_line "geometor.render.plotter.Plotter.plot_line") -> [`Line`](https://docs.sympy.org/latest/modules/geometry/lines.html#sympy.geometry.line.Line "(in SymPy v1.12)")
* [`plot\_circle()`](#geometor.render.plotter.Plotter.plot_circle "geometor.render.plotter.Plotter.plot_circle") -> [`Circle`](https://docs.sympy.org/latest/modules/geometry/ellipses.html#sympy.geometry.ellipse.Circle "(in SymPy v1.12)")




reset\_ax\_all() → [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)")



reset\_ax\_main() → [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)")



reset\_ax\_header() → [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)")



reset\_ax\_footer() → [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)")



set\_ax\_main\_bounds(*bounds*)



annotate\_point(*point: [Point](https://docs.sympy.org/latest/modules/geometry/points.html#sympy.geometry.point.Point "(in SymPy v1.12)")*, *text*)
Annotate the given point with the provided text on the given axes.





plot\_point(*pt: sp\_Point*, *label: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)")*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")
plot the point with corresponding styles
returns a list of artists





plot\_selected\_points(*pts: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[spg.Point]*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")



plot\_circle\_points(*pts: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[spg.Point]*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")



plot\_line(*line: spg.Line*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[mp.Line2D]
returns list of plot artists





plot\_selected\_line(*line: spg.Line*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[mp.Line2D]
returns list of plot artists





plot\_circle(*circle: spg.Circle*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[plt.Circle]
takes a sympy circle and plots with the matplotlib Circle patch





plot\_selected\_circle(*circle: spg.Circle*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[plt.Circle]



plot\_segment(*segment: spg.Segment*, *style\_type: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)") = None*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")



plot\_line\_segment(*line: spg.Line*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")



plot\_circle\_radius(*radius\_segment: spg.Segment*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")



plot\_polygon(*poly: spg.Polygon*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*)
takes a sympy Polygon and plots with the matplotlib Polygon patch





plot\_wedge(*wedge: Wedge*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") = None*) → [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")[mp.patch.Wedge]
takes a geometor.model.Wedge and maps it to a matplotlib patch





plot\_element(*index*, *el*, *model*)
instanstiates and returns a PlotElement object
containing all the necessary matplotlib artifacts for rendering a geometric element





plot\_model(*model: Model*, *annotate\_points=False*)



plot\_header(*text*)
sets up one panel for header





plot\_footer(*index*, *description*, *label*)
sets up 3 panels in footer for index, description and label





set\_plotter\_limits\_from\_points(*points*)



zoom\_to\_points(*zoom\_pts*)



zoom\_to\_bounds()





##### geometor.render.sequencer




*class* geometor.render.sequencer.Sequencer(*plot\_name: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)") | [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)") = None*, *margin=0.1*, *FIG\_W=16*, *FIG\_H=9*)
Bases: [`Plotter`](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")


The Sequencer class encapsulates the setup and generation of geometric
plots. It receives a geometric model and provides functionalities to
sequence and render the plot.



parameters:
`plot\_name`[`str`](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)")the name of the plot





attributes:plot\_name (str, optional): An optional name for the plot.
margin (float, optional): An optional parameter to control the margins of the plot.
fig (Figure): Matplotlib figure object.
ax (Axes): Matplotlib axes object for the main plot.
ax\_label (Axes): Matplotlib axes object for the label.






plot\_sequence(*model: Model*, *extensions=['svg', 'png']*)
Plots the sequence of all types of elements in layers for the given model.





step\_sequence(*model: Model*)
allow interactive stepping through the model






##### geometor.render.styles


dictionary of style sets for matplotlib




geometor.render.styles.get\_styles(*element\_type*, *classes: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)") | [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)") = None*)



##### geometor.render.titler




*class* geometor.render.titler.Titler(*model: Model | [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)") = None*, *plot\_name: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)") | [None](https://docs.python.org/3.9/library/constants.html#None "(in Python v3.9)") = None*, *margin=0.1*, *FIG\_W=16*, *FIG\_H=9*)
Bases: [`Plotter`](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")


The Titler class is primarily for creating slides with latex rendered or overlays



parameters:
`plot\_name`[`str`](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)")the name of the plot





attributes:model (Model): The geometric model to be processed and plotted.
plot\_name (str, optional): An optional name for the plot.
margin (float, optional): An optional parameter to control the margins of the plot.
fig (Figure): Matplotlib figure object.
ax (Axes): Matplotlib axes object for the main plot.
ax\_label (Axes): Matplotlib axes object for the label.






plot\_title(*title*, *folder*, *filename*, *color='w'*, *size=44*)
TODO: Docstring for plot\_title.



Title:
TODO



Returns:
TODO







plot\_overlay(*title*, *folder*, *filename*, *color='w'*, *size=44*)
TODO: Docstring for plot\_overlay.



Title:
TODO



Returns:
TODO








##### geometor.render.chains




geometor.render.chains.plot\_chain(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *index*, *chain*, *extensions=['svg', 'png']*)
plot the chain then remove it





geometor.render.chains.plot\_chains(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *chains: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")*, *extensions=['svg', 'png']*)



##### geometor.render.colors



###### colors module


functions for working with color





geometor.render.colors.get\_colors(*cmap\_name*, *steps*)
return a list of colors n regular steps from a colormap





##### geometor.render.groups


functions to plot groupings of sections




geometor.render.groups.plot\_group(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *index*, *group*, *description*, *extensions=['svg', 'png']*)
Plot the group then remove it.





geometor.render.groups.plot\_groups(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *groups: [dict](https://docs.python.org/3.9/library/stdtypes.html#dict "(in Python v3.9)")*, *title: [str](https://docs.python.org/3.9/library/stdtypes.html#str "(in Python v3.9)")*, *extensions=['svg', 'png']*)



##### geometor.render.sections


functions to plot sections identified in the model


a section is defined as three point along a line




geometor.render.sections.plot\_section(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *index*, *section*, *extensions=['svg', 'png']*)
plot the section then remove it





geometor.render.sections.plot\_sections(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *sections: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")*, *extensions=['svg', 'png']*)



geometor.render.sections.plot\_all\_sections(*plotter: [Plotter](index.html#geometor.render.plotter.Plotter "geometor.render.plotter.Plotter")*, *model: Model*, *sections: [list](https://docs.python.org/3.9/library/stdtypes.html#list "(in Python v3.9)")*, *extensions=['svg', 'png']*)



##### geometor.render.utils


functions to plot utils




geometor.render.utils.set\_bounds(*limx*, *limy*) → [Polygon](https://docs.sympy.org/latest/modules/geometry/polygons.html#sympy.geometry.polygon.Polygon "(in SymPy v1.12)")



geometor.render.utils.snapshot(*folder*, *filename*)



geometor.render.utils.snapshot\_2(*folder*, *filename*, *transparent=False*)



geometor.render.utils.display(*filename*)



geometor.render.utils.adjust\_ratio(*w*, *h*, *ratio*)



geometor.render.utils.adjust\_lims(*limx*, *limy*, *margin\_ratio=0.1*)



geometor.render.utils.get\_limits\_from\_points(*pts*)
find x, y limits from a set of points





geometor.render.utils.ax\_set\_bounds(*ax*, *bounds*)



geometor.render.utils.ax\_set\_spines(*ax*)







### demos




#### demo



```


```






### references




#### sympy




#### matplotlib




#### textualize






### todos




### glossary



testa test item








## indices


* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)







