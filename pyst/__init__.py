import pyst.geometry as geometry
import pyst.solid_angle as solid_angle

from pyst.geometry import *
from pyst.solid_angle import *

try:
    from pyst import plots
except ImportError as e:
    print("Exception raised importing plots package, skipped (you probably need to install matplotlib)")
    print("\n\nException raised: {}".format(e))  
