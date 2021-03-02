import numpy as np

from first_order_params_conf import *
from ocelot.cpbd.transformations.transfer_map import TransferMap, TMTypes
from ocelot.cpbd.elements.drift_atom import DriftAtom
from ocelot.cpbd.elements.marker_atom import MarkerAtom
from ocelot.cpbd.elements.monitor_atom import MonitorAtom
from ocelot.cpbd.elements.quadrupole_atom import QuadrupoleAtom
from ocelot.cpbd.elements.sbend_atom import SBendAtom
from ocelot.cpbd.elements.undulator_atom import UndulatorAtom
from ocelot.cpbd.elements.cavity_atom import CavityAtom
from ocelot.cpbd.elements.sextupole_atom import SextupoleAtom
from ocelot.cpbd.elements.solenoid_atom import SolenoidAtom
from ocelot.cpbd.elements.hcor_atom import HcorAtom
from ocelot.cpbd.elements.vcor_atom import VcorAtom

from ocelot.cpbd.elements.element import Element


def first_order_test(element: Element, name: str, ground_truth_data: Data, tm_type=TMTypes.MAIN):
    tm = TransferMap.create(element, tm_type=tm_type)

    for energy, R_ground_truth, B_ground_truth in ground_truth_data.zip(name):
        params = tm.get_params(energy=energy)
        assert np.allclose(params.R, R_ground_truth, rtol=1e-05, atol=1e-08, equal_nan=False)
        assert np.allclose(params.B, B_ground_truth, rtol=1e-05, atol=1e-08, equal_nan=False)


def test_first_order_drift(load_ground_truth_data):
    first_order_test(DriftAtom(l=0.1586084195, eid='D_103'), 'Drift', load_ground_truth_data)


def test_first_order_marker(load_ground_truth_data):
    first_order_test(MarkerAtom(eid='STSEC.23.I1'), 'Marker', load_ground_truth_data)


def test_first_order_quadrupole(load_ground_truth_data):
    first_order_test(QuadrupoleAtom(l=0.3, k1=-1.537886, tilt=0.0, eid='Q.37.I1'), 'Quadrupole', load_ground_truth_data)


def test_first_order_sbend_entrance(load_ground_truth_data):
    first_order_test(SBendAtom(l=0.200330283531, angle=-0.099484, e1=0.0, e2=-0.099484, tilt=0.0, fint=0.0, eid='BL.48I.I1'), 'SBend_E1', load_ground_truth_data, tm_type=TMTypes.ENTRANCE)


def test_first_order_sbend_main(load_ground_truth_data):
    first_order_test(SBendAtom(l=0.200330283531, angle=-0.099484, e1=0.0, e2=-0.099484, tilt=0.0, fint=0.0, eid='BL.48I.I1'), 'SBend', load_ground_truth_data)


def test_first_order_sbend_exit(load_ground_truth_data):
    first_order_test(SBendAtom(l=0.200330283531, angle=-0.099484, e1=0.0, e2=-0.099484, tilt=0.0, fint=0.0, eid='BL.48I.I1'), 'SBend_E2', load_ground_truth_data, tm_type=TMTypes.EXIT)


def test_first_order_undulator(load_ground_truth_data):
    first_order_test(UndulatorAtom(lperiod=0.074, nperiods=10, Kx=1.36*1.414213, Ky=0.0, eid='UNDU.49.I1'), 'Undulator', load_ground_truth_data)


def test_first_order_cavity_entrance(load_ground_truth_data):
    #Test doesn't make since because if vxx_up or vxy_up isn't set transformation ist eye(6)
    first_order_test(CavityAtom(l=1.0377, v=0.01815975, freq=1.3e9, phi=0.0, eid='C.A1.1.1.I1'), 'Cavity_CK1', load_ground_truth_data, tm_type=TMTypes.ENTRANCE)


def test_first_order_cavity_main(load_ground_truth_data):
    first_order_test(CavityAtom(l=1.0377, v=0.01815975, freq=1.3e9, phi=0.0, eid='C.A1.1.1.I1'), 'Cavity', load_ground_truth_data)


def test_first_order_cavity_exit(load_ground_truth_data):
    #Test doesn't make since because if vxx_down or vxy_down isn't set transformation ist eye(6)
    first_order_test(CavityAtom(l=1.0377, v=0.01815975, freq=1.3e9, phi=0.0, eid='C.A1.1.1.I1'), 'Cavity_CK2', load_ground_truth_data, tm_type=TMTypes.EXIT)


def test_first_order_monitor(load_ground_truth_data):
    first_order_test(MonitorAtom(eid='BPMG.24.I1'), 'Monitor', load_ground_truth_data)


def test_first_order_undulator(load_ground_truth_data):
    first_order_test(UndulatorAtom(lperiod=0.074, nperiods=10, Kx=1.36*1.414213, Ky=0.0, eid='UNDU.49.I1'), 'Undulator', load_ground_truth_data)


def test_first_order_sextupole(load_ground_truth_data):
    first_order_test(SextupoleAtom(l=0.1, k2=1 * -9.817522762, tilt=1.570796327, eid='SC.74I.I1'), 'Sextupole', load_ground_truth_data)


def test_first_order_solenoid(load_ground_truth_data):
    first_order_test(SolenoidAtom(l=0.0, k=0.0, eid='SOLB.23.I1'), 'Solenoid', load_ground_truth_data)


def test_first_order_hcor(load_ground_truth_data):
    first_order_test(HcorAtom(l=0.1, angle=0.0, eid='CIX.102.I1'), 'Hcor', load_ground_truth_data)


def test_first_order_vcor(load_ground_truth_data):
    first_order_test(VcorAtom(l=0.1, angle=0.0, eid='CIX.102.I1'), 'Vcor', load_ground_truth_data)