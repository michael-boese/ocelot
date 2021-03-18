import enum
from copy import deepcopy, copy
import logging
from sys import flags
from typing import Callable, Union
from abc import ABC, abstractmethod

import numpy as np

from ocelot.cpbd.beam import Twiss, Particle, ParticleArray
from ocelot.cpbd.elements.element import Element

_logger = logging.getLogger(__name__)


class TMTypes(enum.Enum):
    ROT_ENTRANCE = 1
    ROT_EXIT = 2
    ENTRANCE = 3
    EXIT = 4
    MAIN = 5


class Transformation(ABC):
    """
    TransferMap is a basic class of all TransferMaps and defines the Interface for them.
    """

    def __init__(self, create_tm_param_func, delta_e_func, tm_type: TMTypes, length: float, delta_length: float = None) -> None:
        """[summary]

        Args:
            create_tm_param_func ([type]): [description]
            length (float): total length to which the transformation is applied.
        """
        self.create_tm_param_func = create_tm_param_func
        self.length = length if tm_type == TMTypes.MAIN else 0.0  # entrance/exit functions (e.g Edges or Couplerkicks) do not have a length.
        self.delta_length = delta_length
        self._delta_e_func = delta_e_func if tm_type == TMTypes.MAIN else None  # entrance/exit functions (e.g Edges or Couplerkicks) do not change beam energy.
        self.tm_type = tm_type

        self._current_energy = None  # used for caching tm params
        self._params = None

        self._map = None

    def _clean_cashed_values(self):
        self._current_energy = None  # used for caching tm params
        self._params = None


    def get_delta_e(self):
        if self._delta_e_func:
            return self._delta_e_func(delta_length=self.delta_length, total_length=self.length)
        else:
            return 0.0

    @classmethod
    @abstractmethod
    def from_element(cls, element: Element, tm_type: TMTypes = TMTypes.MAIN, delta_l: float = None, **params):
        """[summary]
        This classmentod is mainly used to create a new transforamtion from a element. 
        With 'params' custom parameter can be added to the Transformation. 
        :param element: Element for which the transformation is calculated
        :type element: Element
        :param tm_type: Type of Transformation can be TMTypes.ENTRANCE, TMTypes.MAIN or TMTypes.EXIT, defaults to TMTypes.MAIN
        :type tm_type: TMTypes, optional
        :param delta_l: If the parameter is set, just a section of the element is taken into account for the tm calculation, defaults to None
        :type delta_l: float, optional
        :raises NotImplementedError: Have to be implemented by concret transforamtions
        """
        raise NotImplementedError

    @classmethod
    def create(cls, main_tm_params_func, delta_e_func, length, delta_length=None, entrance_tm_params_func=None, exit_tm_params_func=None, tm_type: TMTypes = TMTypes.MAIN, **params):
        try:
            if tm_type == TMTypes.ENTRANCE:
                tm_params_func = entrance_tm_params_func
            elif tm_type == TMTypes.MAIN:
                tm_params_func = main_tm_params_func
            elif tm_type == TMTypes.EXIT:
                tm_params_func = exit_tm_params_func
            if not tm_params_func:
                raise NotImplementedError(f"{'entrance' if tm_type == TMTypes.ENTRANCE else 'exit'} function is not set in {cls.__class__.__name__}'s __init__")
        except AttributeError:
            raise NotImplementedError(f"The specific element have to implement the function {tm_params_func.__name__}.")
        if delta_length and (delta_length > length):
            _logger.warning("delta_l > length of element. Set delta_l == length of element.")
            delta_length = length
        return cls(create_tm_param_func=tm_params_func, delta_e_func=delta_e_func, tm_type=tm_type, length=length, delta_length=delta_length, **params)

    def get_params(self, energy: float):
        if not self._params or self._current_energy != energy:
            self._params = self.create_tm_param_func(energy, self.delta_length)
            self._current_energy = energy
        return self._params

    def apply(self, prcl_series):
        """
        :param prcl_series: can be list of Particles [Particle_1, Particle_2, ... ] or ParticleArray
        :return: None
        """
        if prcl_series.__class__ == ParticleArray:
            self.map_function(self.length, self.delta_length)(prcl_series.rparticles, energy=prcl_series.E)
            #self.map(prcl_series.rparticles, energy=prcl_series.E)
            prcl_series.E += self.get_delta_e()
            #prcl_series.E += self.delta_e
            prcl_series.s += self.length

        elif prcl_series.__class__ == Particle:
            p = prcl_series
            p.x, p.px, p.y, p.py, p.tau, p.p = self.map(np.array([[p.x], [p.px], [p.y], [p.py], [p.tau], [p.p]]), p.E)[
                :, 0]
            p.s += self.length
            p.E += self.get_delta_e()

        elif prcl_series.__class__ == list and prcl_series[0].__class__ == Particle:
            # If the energy is not the same (p.E) for all Particles in the list of Particles
            # in that case cycle is applied. For particles with the same energy p.E
            list_e = np.array([p.E for p in prcl_series])
            if False in (list_e[:] == list_e[0]):
                for p in prcl_series:
                    self.map(np.array([[p.x], [p.px], [p.y], [p.py], [p.tau], [p.p]]), energy=p.E)

                    p.E += self.get_delta_e()
                    p.s += self.length
            else:
                pa = ParticleArray()
                pa.list2array(prcl_series)
                pa.E = prcl_series[0].E
                self.map(pa.rparticles, energy=pa.E)
                pa.E += self.get_delta_e()
                pa.s += self.length
                pa.array2ex_list(prcl_series)

        else:
            _logger.error(" TransferMap.apply(): Unknown type of Particle_series: " + str(prcl_series.__class__.__name))
            raise Exception(
                " TransferMap.apply(): Unknown type of Particle_series: " + str(prcl_series.__class__.__name))

    @abstractmethod
    def map_function(self, delta_length: float = None, length: float = None):
        """[summary]
        This function calculate the transformation. It have to be overloaded by each transformation class.
        :param delta_length: delta length of the element. If set the map function is calculated for delta length, defaults to None
        :type delta_length: float, optional
        :param length: total length of the element, some map functions may need the total length for calculation, defaults to None
        :type length: float, optional
        :return: a Callable (e.g Lambda) which takes a array of particales as the first and the engery as a second parameter.
        :rtype: Callable[np.ndarray, float]
        """
        raise NotImplementedError()

    # @abstractmethod
    # def __mul__(self, m: Union[Particle, 'TransferMap', Twiss]) -> Union[Particle, 'TransferMap', Twiss]:
    #     """[summary]
    #     A Transfermap can be multiplied by Particle, Twiss parameter or by a other TransferMap.
    #     :param m: a Particle, Twiss or TransferMap
    #     :type m: Particle, Twiss, TransferMap
    #     :return: a new Particle, Twiss or TransferMap
    #     :rtype: TransferMap, 'TransferMap', Twiss
    #     """
    #     pass
