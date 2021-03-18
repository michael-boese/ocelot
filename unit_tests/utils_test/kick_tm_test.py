import json

import numpy as np

from ocelot.cpbd.elements.drift import Drift
from ocelot.cpbd.elements.sbend import SBend
from ocelot.cpbd.transformations.kick import KickTM
from ocelot.cpbd.io import load_particle_array

def compare_p_array(p_array, p_array_ground_truth):
    assert p_array.n == p_array_ground_truth.n
    assert np.allclose(p_array.q_array, p_array_ground_truth.q_array, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.rparticles, p_array_ground_truth.rparticles, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.s, p_array_ground_truth.s, rtol=1e-05, atol=1e-08, equal_nan=False)
    assert np.allclose(p_array.t, p_array_ground_truth.t, rtol=1e-05, atol=1e-08, equal_nan=False)

def test_kick_tm_with_drift():
    p_array = load_particle_array("unit_tests/test_data/init_beam.npz")
    with open("unit_tests/test_data/kick_tm/kick_tm_Drift_output.json") as fs:
        drift_params = json.load(fs)
    drift = Drift(**drift_params, tm=KickTM)
    for tm in drift.tms:
        tm.apply(p_array)
    ground_truth = load_particle_array("unit_tests/test_data/kick_tm/kick_tm_Drift_output_0.npz")
    compare_p_array(p_array, ground_truth)    

def test_kick_tm_with_sbend():
    p_array = load_particle_array("unit_tests/test_data/init_beam.npz")
    with open("unit_tests/test_data/kick_tm/kick_tm_SBend_output.json") as fs:
        params = json.load(fs)
    drift = SBend(**params, tm=KickTM)
    for i, tm in enumerate(drift.tms):
        tm.apply(p_array)
        ground_truth = load_particle_array(f"unit_tests/test_data/kick_tm/kick_tm_SBend_output_{i}.npz")
        compare_p_array(p_array, ground_truth)    