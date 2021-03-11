from copy import copy

import numpy as np

from ocelot.cpbd.transformations.transfer_map import TransferMap
from ocelot.cpbd.transformations.tm_utils import SecondOrderMult, transform_vec_ent, transform_vec_ext, \
    transfer_map_rotation, sym_matrix
from ocelot.cpbd.r_matrix import rot_mtx


class SecondTM(TransferMap):
    def __init__(self, r_z_no_tilt, t_mat_z_e):
        TransferMap.__init__(self)
        self.r_z_no_tilt = r_z_no_tilt
        self.t_mat_z_e = t_mat_z_e

        self.multiplication = None

        self.R_tilt = lambda energy: np.dot(np.dot(rot_mtx(-self.tilt), self.r_z_no_tilt(self.length, energy)),
                                            rot_mtx(self.tilt))

        self.T_tilt = lambda energy: transfer_map_rotation(self.r_z_no_tilt(self.length, energy),
                                                           self.t_mat_z_e(self.length, energy), self.tilt)[1]

    @classmethod
    def create_from_element(cls, element, params=None):
        T_z_e = element.get_T_z_e_func()
        tm = cls(r_z_no_tilt=element.create_r_matrix(), t_mat_z_e=T_z_e)
        tm.multiplication = SecondOrderMult().tmat_multip
        return tm

    def calculate_Tb(self, energy) -> np.ndarray:
        """
        Calculates the Tb matrix which is needed to calculate the transfromation matrix.
        @return: Tb matrix
        """
        Tb = np.copy(self.T_tilt(energy))
        Tb = sym_matrix(Tb)
        return Tb

    def t_apply(self, R, T, X, dx, dy, tilt, U5666=0.):
        if dx != 0 or dy != 0 or tilt != 0:
            X = transform_vec_ent(X, dx, dy, tilt)
        self.multiplication(X, R, T)
        if dx != 0 or dy != 0 or tilt != 0:
            X = transform_vec_ext(X, dx, dy, tilt)

        return X

    def map_function(self, delta_length=None, length=None):
        return lambda X, energy: self.t_apply(self.r_z_no_tilt(delta_length if delta_length else self.length, energy), self.t_mat_z_e(delta_length if delta_length else self.length, energy), X, self.dx, self.dy, self.tilt)

    def __call__(self, s):
        m = copy(self)
        m.R = lambda energy: m.R_z(s, energy)
        m.B = lambda energy: m.B_z(s, energy)
        m.T = lambda s, energy: m.t_mat_z_e(s, energy)
        m.delta_e = m.delta_e_z(s)
        m.map = m.map_function(delta_length=s, length=self.length)
        m.length = s
        return m
