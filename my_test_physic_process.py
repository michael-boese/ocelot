# this python library provides generic shallow (copy) and
# deep copy (deepcopy) operations
from copy import deepcopy

import matplotlib.pyplot as plt
import time

# import from Ocelot main modules and functions
from ocelot import *

# import from Ocelot graphical modules
from ocelot.gui.accelerator import *

# import injector lattice
from demos.ipython_tutorials.injector_lattice import *

# initialization of tracking method
method = MethodTM()

# for second order tracking we have to choose SecondTM 
method.global_method = TransferMap

# for first order tracking uncomment next line
# method.global_method = TransferMap

p_array_init = load_particle_array("demos/ipython_tutorials/sc_beam.npz")

# we start simulation from the first quadrupole (QI.46.I1) after RF section.
# you can change stop element (and the start element, as well) 
# START_73_I1 - marker before Dog leg
# START_96_I1 - marker before Bunch Compresion
lat_t = MagneticLattice(cell, start=start_sim, stop=None, method=method)

tw = Twiss()
tw.beta_x = 2.36088
tw.beta_y = 2.824
tw.alpha_x = 1.2206
tw.alpha_y = -1.35329
bt = BeamTransform(tws=tw)

navi = Navigator(lat_t)
p_array = deepcopy(p_array_init)
start = time.time()
tws_track, p_array = track(lat_t, p_array, navi)
print("\n time exec:", time.time() - start, "sec")

# you can change top_plot argument, for example top_plot=["alpha_x", "alpha_y"]
plot_opt_func(lat_t, tws_track, top_plot=["E"], fig_name=0, legend=False)
plt.show()

# navi = Navigator(lat_t)
# navi.unit_step = 0.5 # ignored in that case, tracking will performs element by element.
#                    # - there is no PhysicsProc along the lattice,
#                    # BeamTransform is aplied only once
# navi.add_physics_proc(bt, OTRC_55_I1, OTRC_55_I1)
# empty = PhysProc()
# navi.add_physics_proc(empty, start_sim, END_119_I1)
# p_array = deepcopy(p_array_init)
# start = time.time()
# tws_track, p_array = track(lat_t, p_array, navi)
# print("\n time exec:", time.time() - start, "sec")
# plot_opt_func(lat_t, tws_track, top_plot=["E"], fig_name=0, legend=False)
# plt.show()