import json

import numpy as np

from ocelot.cpbd.elements.drift import Drift
from ocelot.cpbd.elements.undulator import Undulator
from ocelot.cpbd.transformations.runge_kutta import RungeKuttaTM
from ocelot.cpbd.io import load_particle_array


def compare_p_array(p_array, p_array_ground_truth):
    assert p_array.n == p_array_ground_truth.n
    assert np.allclose(p_array.q_array, p_array_ground_truth.q_array, rtol=1e-05, atol=1e-08, equal_nan=True)
    assert np.allclose(p_array.rparticles, p_array_ground_truth.rparticles, rtol=1e-05, atol=1e-08, equal_nan=True)
    assert np.allclose(p_array.s, p_array_ground_truth.s, rtol=1e-05, atol=1e-08, equal_nan=True)
    assert np.allclose(p_array.t, p_array_ground_truth.t, rtol=1e-05, atol=1e-08, equal_nan=True)


def test_runge_kutta_tm_with_undulator():
    p_array = load_particle_array("unit_tests/test_data/init_beam.npz")
    with open("unit_tests/test_data/runge_kutta_tm/runge_kutta_tm_Undulator_output.json") as fs:
        params = json.load(fs)
    und = Undulator(**params, tm=RungeKuttaTM)
    for tm in und.tms:
        tm.apply(p_array)
    ground_truth = load_particle_array("unit_tests/test_data/runge_kutta_tm/runge_kutta_tm_Undulator_output_0.npz")
    compare_p_array(p_array, ground_truth)
