"""
The Render Module
provides functions for plotting elements from the geometric model to
matplotlib.
"""
__author__ = "geometor"
__maintainer__ = "geometor"
__email__ = "github@geometor.com"
__version__ = "0.0.1"
__licence__ = "MIT"

from .common import *

from geometor.model import *
from geometor.model.utils import *

from .utils import *

from .plotter import *
from .sections import *
from .chains import *
from .groups import *
from .sequencer import *
from .titler import *


# TODO: move to divine -extend sequencer to render sections
#  from .sections import *
#  from .groups import *
#  from .ranges import *
