``geometor.render`` is the foundational library for the GEOMETOR_ initiative for visualization.

Additional information about ``geometor.render`` can be seen at the `Project's Website`_


* Contents:

  + 1 mission_
  + 2 overview_
  + 3 installation_
  + 4 usage_
  + 5 dependencies_
  + 6 contributing_
  + 7 license_

mission
-------

The mission of this module is to establish a rigorous system for defining
classical geometric constructions of points, lines and circles. But in our
case, we are not using straight edge and compass. We are creating the geometric
elements as expressions in symbolic algebra thanks to the power of the `Sympy`_
library.





installation
------------

You can install ``geometor.render`` using pip:

.. code-block:: bash

   pip install geometor-render

or clone this repo and install it directly.

.. code-block:: bash

   git clone https://github.com/geometor/render
   cd render
   pip install -e .


usage
-----
- [ ] test

.. code-block:: python

    from geometor.model import *
    from geometor.render import *


    model = Model("vesica")
    A = model.set_point(0, 0, classes=["given"])
    B = model.set_point(1, 0, classes=["given"])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    model.construct_circle(B, A)

    E = model.get_element_by_label("E")
    F = model.get_element_by_label("F")

    model.set_polygon([A, B, E])
    model.set_polygon([A, B, F])

    model.construct_line(E, F)

    report_summary(model)
    report_group_by_type(model)
    report_sequence(model)

    model.save("vesica.json")


After installation, you can use the ``render`` command to create a new project:

.. code-block:: bash

   render 

.. todo:: TODO: list arguments

dependencies
------------

**render** depends on the following Python packages:

.. todo:: TODO: read from pyproject.toml 

contributing
------------

Contributions are welcome! Please see our [GitHub issues](https://github.com/geometor/render/issues) for ways to contribute.

license
-------

**render** is licensed under the MIT License. See the `LICENSE` file for more details.
