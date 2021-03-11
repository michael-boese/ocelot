# this python library provides generic shallow (copy) and
# deep copy (deepcopy) operations
from copy import deepcopy

import matplotlib.pyplot as plt
import time

# import from Ocelot main modules and functions
from ocelot import *

from ocelot.cpbd.io import save_particle_array2npz

# import from Ocelot graphical modules
from ocelot.gui.accelerator import *

# import injector lattice
from demos.ipython_tutorials.injector_lattice import *

method = MethodTM()
# for second order tracking we have to choose SecondTM
method.global_method = TransferMap
# for first order tracking uncomment next line
# method.global_method = TransferMap
p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")


lat_t = MagneticLattice(cell, start=start_sim, stop=None, method=method)

start = Marker()
# c = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
#         CKY_23_I1, D_3, BPMG_24_I1, D_4, SCRN_24_I1, FCUP_24_I1, D_5, ENSUB_24_I1,
#         STSUB_24_I1, D_6, CKX_24_I1, CKY_24_I1, D_7, TORA_25_I1, D_8, SCRN_25I_I1,
#         FCUP_25I_I1, D_9, BPMG_25I_I1, D_10, DCM_25_I1, D_11, CKX_25_I1, CKY_25_I1,
#         D_12, START_25_I1, D_13, STAC_26_I1, D_14, C_A1_1_1_I1, D_15, C_A1_1_2_I1,
#         D_16, C_A1_1_3_I1, D_17, C_A1_1_4_I1, D_18, C_A1_1_5_I1, D_19, C_A1_1_6_I1,
#         D_20, C_A1_1_7_I1, D_21, C_A1_1_8_I1, D_22, stop_A1, Q_37_I1, CX_37_I1, CY_37_I1,
#         D_23, BPMC_38I_I1, D_24, ENAC_38_I1, STAC_38_I1, D_25, BPMR_38II_I1, D_26,
#         Q_38_I1, CX_39_I1, CY_39_I1, D_27, C3_AH1_1_1_I1, D_28, C3_AH1_1_2_I1, D_29,
#         C3_AH1_1_3_I1, D_30, C3_AH1_1_4_I1, D_31, C3_AH1_1_5_I1, D_32, C3_AH1_1_6_I1, D_33,
#         C3_AH1_1_7_I1, D_34, C3_AH1_1_8_I1, D_35, ENAC_44_I1, D_36, END_45_I1, D_37,
#         TORA_46_I1, D_38, QI_46_I1, D_39, BAM_47_I1, D_40, BPMF_47_I1, D_41,
#         MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]

# c = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
#      CKY_23_I1, D_3, BPMG_24_I1, D_4, SCRN_24_I1, FCUP_24_I1, D_5, ENSUB_24_I1,
#      STSUB_24_I1, D_6, CKX_24_I1, CKY_24_I1, D_7, TORA_25_I1, D_8, SCRN_25I_I1,
#      FCUP_25I_I1, D_9, BPMG_25I_I1, D_10, DCM_25_I1, D_11, CKX_25_I1, CKY_25_I1,
#      D_12, START_25_I1, D_13, STAC_26_I1, D_14, C_A1_1_1_I1, D_15, C_A1_1_2_I1,
#      D_16, C_A1_1_3_I1, D_17, C_A1_1_4_I1, D_18, C_A1_1_5_I1, D_19, C_A1_1_6_I1,
#      D_20, C_A1_1_7_I1, D_21, C_A1_1_8_I1, D_35, ENAC_44_I1, D_36, END_45_I1, D_37,
#      TORA_46_I1, D_38, QI_46_I1, D_39, BAM_47_I1, D_40, BPMF_47_I1, D_41,
#      MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]

#c = [D_21, C_A1_1_8_I1, D_45, BL_48I_I1, D_46]

#c = [D_21, C_A1_1_8_I1, D_45, BL_48I_I1, D_33]

#c = [D_21, C_A1_1_8_I1, D_45, BL_73_I1, D_33]

#lat_t = MagneticLattice(c, start=None, stop=None, method=method)
navi = Navigator(lat_t)

p_array = deepcopy(p_array_init)
start = time.time()
tws_track, p_array = track(lat_t, p_array, navi)
print("\n time exec:", time.time() - start, "sec")
# you can change top_plot argument, for example top_plot=["alpha_x", "alpha_y"]
plot_opt_func(lat_t, tws_track, top_plot=["E"], fig_name=0, legend=False)
plt.show()