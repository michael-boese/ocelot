# this python library provides generic shallow (copy) and 
# deep copy (deepcopy) operations 
from copy import deepcopy

import time

# import from Ocelot main modules and functions
from ocelot import *

# import from Ocelot graphical modules
from ocelot.gui.accelerator import *

# import injector lattice
from demos.ipython_tutorials.injector_lattice import *

lat = MagneticLattice(cell, stop=None)

# initialization of Twiss object
tws0 = Twiss()
# defining initial twiss parameters
tws0.beta_x = 29.171
tws0.beta_y = 29.171
tws0.alpha_x = 10.955
tws0.alpha_y = 10.955
# defining initial electron energy in GeV
tws0.E = 0.005 

# calculate optical functions with initial twiss parameters
tws = twiss(lat, tws0, nPoints=None)

plot_opt_func(lat, tws, top_plot=["Dx", "Dy"], fig_name="i1", legend=False)
plt.show()