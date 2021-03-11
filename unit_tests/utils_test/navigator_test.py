# this python library provides generic shallow (copy) and
# deep copy (deepcopy) operations
from copy import deepcopy
from pathlib import Path

import matplotlib.pyplot as plt
import time

# import from Ocelot main modules and functions
from ocelot import *

# import from Ocelot graphical modules
from ocelot.gui.accelerator import *

# import injector lattice
from demos.ipython_tutorials.injector_lattice import *


def compare_p_array(p_array, p_array_ground_truth):
    assert p_array.n == p_array_ground_truth.n
    assert np.allclose(p_array.q_array, p_array_ground_truth.q_array, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.rparticles, p_array_ground_truth.rparticles, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.s, p_array_ground_truth.s, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.t, p_array_ground_truth.t, rtol=1e-05, atol=1e-08, equal_nan=False)


def get_maps_from_single_element_lat_test(p_array_init, element, method):
    lat_t = MagneticLattice([element], start=None, stop=None, method=method)

    tw = Twiss()
    tw.beta_x = 2.36088
    tw.beta_y = 2.824
    tw.alpha_x = 1.2206
    tw.alpha_y = -1.35329
    bt = BeamTransform(tws=tw)
    navi = Navigator(lat_t)

    p_array = deepcopy(p_array_init)
#    tms = [tms for tms, _, _, _ in navi.get_next_step()]
#    for i, t_map in enumerate([tm for sub_tms in tms for tm in sub_tms]):
    for tms, _, _, _ in navi.get_next_step():
        for t_map in tms:
            t_map.apply(p_array)
    p_array_ground_truth = load_particle_array(f"unit_tests/test_data/ground_truth_{element.__class__.__name__}_output.npz")

    compare_p_array(p_array, p_array_ground_truth)


def test_get_maps_single_SBend_lat():
    method = MethodTM()

    # for second order tracking we have to choose SecondTM
    method.global_method = TransferMap

    # for first order tracking uncomment next line
    # method.global_method = TransferMap

    p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")

    get_maps_from_single_element_lat_test(p_array_init, SBend(l=0.200330283531, angle=-0.1109740393, e1=-0.05548702, e2=-0.05548702, tilt=0.0, fint=0.0, eid='BL.48I.I1'), method)


def test_get_maps_Drift_lat():
    method = MethodTM()

    # for second order tracking we have to choose SecondTM
    method.global_method = TransferMap

    # for first order tracking uncomment next line
    # method.global_method = TransferMap

    p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")

    drift = Drift(l=0.474, eid='D_2')

    get_maps_from_single_element_lat_test(p_array_init, drift, method)


def test_get_maps_Marker_lat():
    method = MethodTM()

    # for second order tracking we have to choose SecondTM
    method.global_method = TransferMap

    # for first order tracking uncomment next line
    # method.global_method = TransferMap

    p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")

    m = Marker(eid='STSEC.23.I1')

    get_maps_from_single_element_lat_test(p_array_init, m, method)


def test_plot():
    method = MethodTM()
    # for second order tracking we have to choose SecondTM
    method.global_method = TransferMap
    # for first order tracking uncomment next line
    # method.global_method = TransferMap
    p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")
    lat_t = MagneticLattice(cell, start=start_sim, stop=None, method=method)
    navi = Navigator(lat_t)
    p_array = deepcopy(p_array_init)
    start = time.time()
    tws_track, p_array = track(lat_t, p_array, navi)
    print("\n time exec:", time.time() - start, "sec")
    # you can change top_plot argument, for example top_plot=["alpha_x", "alpha_y"]
    plot_opt_func(lat_t, tws_track, top_plot=["E"], fig_name=0, legend=False)
    plt.show()
    assert False

def test_maps_of_fel():
    method = MethodTM()

    # for second order tracking we have to choose SecondTM
    method.global_method = TransferMap

    # for first order tracking uncomment next line
    # method.global_method = TransferMap

    p_array_init = load_particle_array("unit_tests/test_data/init_beam.npz")

    lat_t = MagneticLattice(cell, start=start_sim, stop=None, method=method)

    tw = Twiss()
    tw.beta_x = 2.36088
    tw.beta_y = 2.824
    tw.alpha_x = 1.2206
    tw.alpha_y = -1.35329
    bt = BeamTransform(tws=tw)
    navi = Navigator(lat_t)

    ground_truth_filepaths = [p for p in Path('unit_tests/test_data').glob("**/ground_truth_output_*.npz")]
    ground_truth_filepaths_sorted_by_num = sorted(ground_truth_filepaths, key=lambda s: int(s.stem.split('_')[-1]))


    p_array = deepcopy(p_array_init)
    i = 0
    gt_i = 0
    for tms, _, _, _ in navi.get_next_step():
        name = lat_t.sequence[i].__class__.__name__
        print(name)
        # if name == "Cavity":
        #     assert len(tms) == 3
        #     tms[0].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_CouplerKick_{gt_i}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     tms[1].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_{name}_{gt_i+1}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     tms[2].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_CouplerKick_{gt_i+2}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     gt_i += 2

        # if name in ["Bend", "SBend", "RBend"]:
        #     assert len(tms) == 3
        #     tms[0].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_Edge_{gt_i}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     tms[1].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_{name}_{gt_i+1}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     tms[2].apply(p_array)
        #     data_name = f"unit_tests/test_data/ground_truth_output_Edge_{gt_i+2}.npz"
        #     p_array_ground_truth = load_particle_array(data_name)
        #     compare_p_array(p_array, p_array_ground_truth)
        #     gt_i += 2

        for t_map in tms:
            t_map.apply(p_array)
            data_name = ground_truth_filepaths_sorted_by_num[gt_i]
            p_array_ground_truth = load_particle_array(data_name)
            compare_p_array(p_array, p_array_ground_truth)
            i += 1
            gt_i += 1

    # tms = (tms for tms, _, _, _ in navi.get_next_step())
    # for i, t_map in enumerate((tm for sub_tms in tms for tm in sub_tms)):
    #     t_map.apply(p_array)
    #     name = navi.lat.sequence[navi.n_elem].__class__.__name__
    #     data_name = f"unit_tests/test_data/ground_truth_output_{name}_{i}.npz"
    #     p_array_ground_truth = load_particle_array(data_name)
    #     print(data_name)

    #     compare_p_array(p_array, p_array_ground_truth)
