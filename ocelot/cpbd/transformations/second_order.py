from copy import copy

import numpy as np
from ocelot.cpbd.tm_utils import SecondOrderMult, transform_vec_ent, transform_vec_ext, \
    transfer_map_rotation, sym_matrix

from ocelot.cpbd.transformations.transformation import Transformation, TMTypes
from ocelot.cpbd.elements.element import Element


class SecondTM(Transformation):
    def __init__(self, create_tm_param_func, delta_e_func, tm_type: TMTypes, length: float, delta_length: float = 0.0) -> None:
        self.multiplication = SecondOrderMult().tmat_multip
        super().__init__(create_tm_param_func, delta_e_func, tm_type, length, delta_length)

    @classmethod
    def from_element(cls, element: Element, tm_type: TMTypes = TMTypes.MAIN, delta_l=None):
        return cls.create(entrance_tm_params_func=element.create_second_order_entrance_params if element.has_edge else None,
                          delta_e_func=element.create_delta_e,
                          main_tm_params_func=element.create_second_order_main_params,
                          exit_tm_params_func=element.create_second_order_exit_params if element.has_edge else None,
                          tm_type=tm_type, length=element.l, delta_length=delta_l)

    def t_apply(self, energy, X, U5666=0.):
        params = self.get_params(energy)
        if params.dx != 0 or params.dy != 0 or params.tilt != 0:
            X = transform_vec_ent(X, params.dx, params.dy, params.tilt)
        self.multiplication(X, params.R, params.T)
        if params.dx != 0 or params.dy != 0 or params.tilt != 0:
            X = transform_vec_ext(X, params.dx, params.dy, params.tilt)

        return X

    def map_function(self, delta_length=None, length=None):
        return lambda X, energy: self.t_apply(energy, X)

    def calculate_Tb(self, energy) -> np.ndarray:
        """
        Calculates the Tb matrix which is needed to calculate the transfromation matrix.
        @return: Tb matrix
        """
        raise NotImplementedError("Not implemented yet")
        T_tilt = transfer_map_rotation(self.r_z_no_tilt(self.length, energy),
                                       self.t_mat_z_e(self.length, energy), self.tilt)[1]
        return sym_matrix(T_tilt)
