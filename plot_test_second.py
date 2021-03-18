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
method.global_method = SecondTM
# for first order tracking uncomment next line
# method.global_method = TransferMap
p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")


lat_t = MagneticLattice(cell, start=start_sim, stop=None, method=method)

start = Marker()
# c = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
#      CKY_23_I1, D_3, BPMG_24_I1, D_4, SCRN_24_I1, FCUP_24_I1, D_5, ENSUB_24_I1,
#      STSUB_24_I1, D_6, CKX_24_I1, CKY_24_I1, D_7, TORA_25_I1, D_8, SCRN_25I_I1,
#      FCUP_25I_I1, D_9, BPMG_25I_I1, D_10, DCM_25_I1, D_11, CKX_25_I1, CKY_25_I1,
#      D_12, START_25_I1, D_13, STAC_26_I1, D_14, C_A1_1_1_I1, D_15, C_A1_1_2_I1,
#      D_16, C_A1_1_3_I1, D_17, C_A1_1_4_I1, D_18, C_A1_1_5_I1, D_19, C_A1_1_6_I1,
#      D_20, C_A1_1_7_I1, D_21, C_A1_1_8_I1, D_22, stop_A1, Q_37_I1, CX_37_I1, CY_37_I1,
#      D_23, BPMC_38I_I1, D_24, ENAC_38_I1, STAC_38_I1, D_25, BPMR_38II_I1, D_26,
#      Q_38_I1, CX_39_I1, CY_39_I1, D_27, C3_AH1_1_1_I1, D_28, C3_AH1_1_2_I1, D_29,
#      C3_AH1_1_3_I1, D_30, C3_AH1_1_4_I1, D_31, C3_AH1_1_5_I1, D_32, C3_AH1_1_6_I1, D_33,
#      C3_AH1_1_7_I1, D_34, C3_AH1_1_8_I1, D_35, ENAC_44_I1, D_36, END_45_I1, D_37,
#      TORA_46_I1, D_38, QI_46_I1, D_39, BAM_47_I1, D_40, BPMF_47_I1, D_41,
#      MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]

# c = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
#      CKY_23_I1, D_3, BPMG_24_I1, D_4, SCRN_24_I1, FCUP_24_I1, D_5, ENSUB_24_I1,
#      STSUB_24_I1, D_6, CKX_24_I1, CKY_24_I1, D_7, TORA_25_I1, D_8, SCRN_25I_I1,
#      FCUP_25I_I1, D_9, BPMG_25I_I1, D_10, DCM_25_I1, D_11, CKX_25_I1, CKY_25_I1,
#      D_12, START_25_I1, D_13, STAC_26_I1, D_14, C_A1_1_1_I1, D_15, C_A1_1_2_I1,
#      D_16, C_A1_1_3_I1, D_17, C_A1_1_4_I1, D_18, C_A1_1_5_I1, D_19, C_A1_1_6_I1,
#      D_20, C_A1_1_7_I1, D_21, C_A1_1_8_I1, D_35, ENAC_44_I1, D_36, END_45_I1, D_37,
#      TORA_46_I1, D_38, QI_46_I1, D_39, BAM_47_I1, D_40, BPMF_47_I1, D_41,
#      MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]


# c = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
#      CKY_23_I1, D_3, BPMG_24_I1, D_4, SCRN_24_I1, FCUP_24_I1, D_5, ENSUB_24_I1,
#      STSUB_24_I1, D_6, CKX_24_I1, CKY_24_I1, D_7, TORA_25_I1, D_8, SCRN_25I_I1,
#      FCUP_25I_I1, D_9, BPMG_25I_I1, D_10, DCM_25_I1, D_11, CKX_25_I1, CKY_25_I1,
#      D_12, START_25_I1, D_13, STAC_26_I1, D_14, C_A1_1_1_I1, D_15, C_A1_1_2_I1,
#      D_16, C_A1_1_3_I1, D_17, C_A1_1_4_I1, D_18, C_A1_1_5_I1, D_19, C_A1_1_6_I1,
#      D_20, C_A1_1_7_I1, D_21, C_A1_1_8_I1] + \
#     [stop_A1, Q_37_I1, CX_37_I1, CY_37_I1,
#      D_23, BPMC_38I_I1, D_24, ENAC_38_I1, STAC_38_I1, D_25, BPMR_38II_I1, D_26,
#      Q_38_I1, CX_39_I1, CY_39_I1] + \
#     [D_35, ENAC_44_I1, D_36, END_45_I1, D_37,
#         TORA_46_I1, D_38, QI_46_I1, D_39, BAM_47_I1, D_40, BPMF_47_I1, D_41,
#         MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]

#c = [D_21, C_A1_1_8_I1, D_45, BL_48I_I1, D_46]

#c = [D_21, C_A1_1_8_I1, D_45, BL_48I_I1, D_33]

# c = [C_A1_1_8_I1, D_21, D_22, stop_A1, Q_37_I1, CX_37_I1, CY_37_I1,
#      D_23, BPMC_38I_I1, D_24, ENAC_38_I1, STAC_38_I1, D_25, BPMR_38II_I1, D_26,
#      Q_38_I1, CX_39_I1, CY_39_I1,  BL_48I_I1, D_33, BL_48II_I1, D_34]

# c = [C_A1_1_8_I1, D_21, D_22, stop_A1, Q_37_I1,
#      D_23, D_24, STAC_38_I1, D_25, D_26,
#      Q_38_I1,  BL_48I_I1, D_33, BL_48II_I1, D_34]

#c = [C_A1_1_8_I1, D_21, D_22, Q_37_I1, D_23, Q_38_I1, D_20, BL_48I_I1, D_33, BL_48II_I1, D_34]

# c = [C_A1_1_8_I1, D_21, CX_37_I1, CY_37_I1,
#      D_23, BPMC_38I_I1, D_24, ENAC_38_I1, STAC_38_I1, D_25, BPMR_38II_I1, D_26,
#      Q_38_I1, CX_39_I1, CY_39_I1,  BL_48I_I1, D_33, BL_48II_I1, D_34]

# c = [D_21, C_A1_1_8_I1] + \
#    [D_27, C3_AH1_1_4_I1] + \
#    [D_45, BL_48I_I1, D_46, BL_48II_I1, D_47]

# C_BREAM = [STSEC_23_I1, STSUB_23_I1, GUN_23_I1, D_1, SOLB_23_I1, D_2, CKX_23_I1,
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
#         MPBPMF_47_I1, D_42, DCM_47_I1, D_43, QI_47_I1, D_44, STLAT_47_I1, D_45,
#         BL_48I_I1, D_46, BL_48II_I1, D_47, MPBPMF_48_I1, D_48, BPMF_48_I1, D_49,
#         OTRL_48_I1, D_50, und_start, UNDU_49_I1, und_stop, D_51, OTRL_50_I1, D_52, BL_50I_I1, D_53,
#         BL_50II_I1, D_54, ENLAT_50_I1, D_55, QI_50_I1, D_56, EOD_51_I1, D_57,
#         CIY_51_I1, D_58, CIX_51_I1, D_59, BPMF_52_I1, D_60, MPBPMF_52_I1, D_61,
#         QI_52_I1, D_62, TDSA_52_I1, D_63, QI_53_I1, D_64, QI_54_I1, D_65,
#         START_55_I1, D_66, OTRC_55_I1]

#start = Marker()
#end = Marker()
#lat_t = MagneticLattice([start, Drift(l=10),end], start=None, stop=None, method=method)

navi = Navigator(lat_t)

tw = Twiss()
tw.beta_x = 2.36088
tw.beta_y = 2.824
tw.alpha_x = 1.2206
tw.alpha_y = -1.35329
bt = BeamTransform(tws=tw)
navi.unit_step = 0.5  # ignored in that case, tracking will performs element by element.
# - there is no PhysicsProc along the lattice,
# BeamTransform is aplied only once
navi.add_physics_proc(bt, OTRC_55_I1, OTRC_55_I1)
empty = PhysProc()
navi.add_physics_proc(empty, start_sim, END_119_I1)

p_array = deepcopy(p_array_init)


start = time.time()
tws_track, p_array = track(lat_t, p_array, navi)
print("\n time exec:", time.time() - start, "sec")
# you can change top_plot argument, for example top_plot=["alpha_x", "alpha_y"]
plot_opt_func(lat_t, tws_track, top_plot=["E"], fig_name=0, legend=False)
plt.show()
