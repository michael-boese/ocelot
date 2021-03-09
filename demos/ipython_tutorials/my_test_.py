# import from Ocelot main modules and functions
from ocelot import *
from ocelot.cpbd.magnetic_lattice import MagneticLattice

# import from Ocelot graphical modules
from ocelot.gui.accelerator import *

# import injector lattice
from injector_lattice import *

import json
import numpy as np

GROUND_TRUTH = {}


def get_tm_params(element, energy_list, res_dict, tm, key_name=None):
    if not key_name:
        key_name = element.__class__.__name__
    method = MethodTM(params={'global': tm})
    lat = MagneticLattice([element], stop=None, method=method)
    lat.update_transfer_maps()
    if element.__class__ in (SBend, Cavity):
        res_dict[f"{key_name}_{'CK1' if element.__class__ == Cavity else 'E1'}"] = {
            'energy_list': energy_list,
            'length': lat.sequence[0].l,
            'tm': lat.sequence[0].transfer_map.__class__.__name__,
            'R': [lat.sequence[0].transfer_map.R_z(lat.sequence[0].l, energy).tolist() for energy in energy_list],
            'B': [lat.sequence[0].transfer_map.B_z(lat.sequence[0].l, energy).tolist() for energy in energy_list],
            'T': [lat.sequence[0].transfer_map.t_mat_z_e(lat.sequence[0].l, energy).tolist() for energy in energy_list]}
        res_dict[f"{key_name}_{'CK2' if element.__class__ == Cavity else 'E2'}"] = {
            'energy_list': energy_list,
            'length': lat.sequence[2].l,
            'tm': lat.sequence[2].transfer_map.__class__.__name__,
            'R': [lat.sequence[2].transfer_map.R_z(lat.sequence[2].l, energy).tolist() for energy in energy_list],
            'B': [lat.sequence[2].transfer_map.B_z(lat.sequence[2].l, energy).tolist() for energy in energy_list],
            'T': [lat.sequence[0].transfer_map.t_mat_z_e(lat.sequence[2].l, energy).tolist() for energy in energy_list]}

    res_dict[key_name] = {
        'energy_list': energy_list,
        'length': element.l,
        'tm': element.transfer_map.__class__.__name__,
        'R': [element.transfer_map.R_z(element.l, energy).tolist() for energy in energy_list],
        'B': [element.transfer_map.B_z(element.l, energy).tolist() for energy in energy_list],
        'T': [lat.sequence[0].transfer_map.t_mat_z_e(element.l, energy).tolist() for energy in energy_list]}


if __name__ == "__main__":
    energy_list = [0.005, 0.13027809280000008, 0.050, 0.5]
    tm = SecondTM

    get_tm_params(Drift(l=0.1586084195, eid='D_103'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Quadrupole(l=0.3, k1=-1.537886, tilt=0.0, eid='Q.37.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(SBend(l=0.200330283531, angle=-0.099484, e1=0.0, e2=-0.099484, tilt=0.0, fint=0.0, eid='BL.48I.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Undulator(lperiod=0.074, nperiods=10, Kx=1.36*1.414213, Ky=0.0, eid='UNDU.49.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Cavity(l=1.0377, v=0.01815975, freq=1.3e9, phi=0.0, eid='C.A1.1.1.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Marker(eid='STSEC.23.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Monitor(eid='BPMG.24.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Sextupole(l=0.1, k2=1 * -9.817522762, tilt=1.570796327, eid='SC.74I.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Solenoid(l=0.0, k=0.0, eid='SOLB.23.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Hcor(l=0.1, angle=0.0, eid='CIX.102.I1'), energy_list, GROUND_TRUTH, tm)
    get_tm_params(Vcor(l=0.1, angle=0.0, eid='CIX.102.I1'), energy_list, GROUND_TRUTH, tm)

    print(GROUND_TRUTH)

    with open('first_oder_param_ground_truth.json', 'w') as fp:
        json.dump(GROUND_TRUTH, fp)

    with open('first_oder_param_ground_truth.json') as fp:
        ground_truth_reloaded = json.load(fp)

    print(type(GROUND_TRUTH['Drift']['R'][0]))

    assert np.allclose(GROUND_TRUTH['Drift']['R'][0], np.array(ground_truth_reloaded['Drift']['R'][0], dtype='float64'), rtol=1e-05, atol=1e-08, equal_nan=False)
    print('test end')
