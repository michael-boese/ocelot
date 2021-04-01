from copy import deepcopy, copy
import logging

import numpy as np

from ocelot.cpbd.transformations.transformation import Transformation, TMTypes
from ocelot.cpbd.elements.element import Element

_logger = logging.getLogger(__name__)


class TransferMap(Transformation):
    """
    TransferMap is a basic linear transfer map for all elements.
    """

    def __init__(self, create_tm_param_func, delta_e_func, tm_type: TMTypes, length: float, delta_length: float = 0.0) -> None:
        super().__init__(create_tm_param_func, delta_e_func, tm_type, length, delta_length)

    @classmethod
    def from_element(cls, element: Element, tm_type: TMTypes = TMTypes.MAIN, delta_l=None):
        return cls.create(entrance_tm_params_func=element.create_first_order_entrance_params if element.has_edge else None,
                          delta_e_func=element.create_delta_e,
                          main_tm_params_func=element.create_first_order_main_params,
                          exit_tm_params_func=element.create_first_order_exit_params if element.has_edge else None,
                          tm_type=tm_type, length=element.l, delta_length=delta_l)

    # @property
    # def map(self):
    #     if not self._map:
    #         self._map = self.map_function()
    #     return self._map

    # @map.setter
    # def map(self, func):
    #     self._map = func

    def map_function(self, delta_length=None, length=None):
        """
        This function calculate the map function which can be overload if the map function is different to the first order mapping  
        @param delta_length: delta length of the element
        @param length: total length of the element
        """
        return lambda u, energy: self.mul_p_array(u, energy=energy)

    def mul_p_array(self, rparticles, energy=0.):
        """
        Calculates new rpaticles with the first order transformation, overrides the old rpaticles and returns the new rparticles. 
        :param rparticles: Can be a ParticleArray, Particle or a list of Particle object. 
        :param engery:
        :return: Returns the modified rparticles 
        """
        params = self.get_params(energy)
        a = np.add(np.dot(params.get_rotated_R(), rparticles), params.B)
        rparticles[:] = a[:]
        return rparticles

    def multiply_with_tm(self, tm: 'TransferMap', length) -> 'TransferMap':
        return TransferMap(create_tm_param_func=lambda energy: self.get_params(energy) * tm.get_params(energy),
                           length=length + tm.length)

    def __mul__(self, m):
        """
        :param m: TransferMap, Particle or Twiss
        :return: TransferMap, Particle or Twiss
        Ma = {Ba, Ra, Ta}
        Mb = {Bb, Rb, Tb}
        X1 = R*(X0 - dX) + dX = R*X0 + B
        B = (E - R)*dX
        """
        try:
            return m.multiply_with_tm(self, self.delta_length if self.delta_length else self.length)
        except AttributeError as e:
            _logger.error(
                " TransferMap.__mul__: unknown object in transfer map multiplication: " + str(m.__class__.__name__))
            raise Exception(
                " TransferMap.__mul__: unknown object in transfer map multiplication: " + str(m.__class__.__name__))

    # TODO: Refactor old style
    # def __call__(self, delta_length):
    #     m = copy(self)
    #     m.R = lambda energy: m.R_z(delta_length, energy)
    #     m.B = lambda energy: m.B_z(delta_length, energy)
    #     m.delta_e = m.delta_e_z(delta_length)
    #     m.map = m.map_function(delta_length=delta_length, length=self.length)
    #     m.length = delta_length
    #     return m

    @classmethod
    def create_from_element(cls, element, params=None):
        return cls()
