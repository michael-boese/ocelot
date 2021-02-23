import enum
from copy import deepcopy, copy
import logging
from typing import Callable, Union
from abc import ABC, abstractmethod
import numpy as np

from ocelot.cpbd.beam import Twiss, Particle, ParticleArray

_logger = logging.getLogger(__name__)


class TMTypes(enum.Enum):
    ENTRANCE = 1
    EXIT = 2
    MAIN = 3


class Transformation(ABC):
    """
    TransferMap is a basic class of all TransferMaps and defines the Interface for them.
    """

    def __init__(self, energy, main_tm_params_func, entrance_tm_params_func=None, exit_tm_params_func=None, tm_type: TMTypes = TMTypes.MAIN) -> None:
        try:
            if tm_type == TMTypes.ENTRANCE:
                tm_params_func = entrance_tm_params_func
            elif tm_type == TMTypes.MAIN:
                tm_params_func = main_tm_params_func
            elif tm_type == TMTypes.EXIT:
                tm_params_func = exit_tm_params_func
            if not tm_params_func:
                raise NotImplementedError(f"{'entrance' if tm_type == TMTypes.ENTRANCE else 'exit'} function is not set in {self.__class__.__name__}'s __init__")
            self.params = tm_params_func(energy)
            self.energy = energy
        except AttributeError:
            raise NotImplementedError(f"The specific element have to implement the function {tm_params_func.__name__}.")
        self._map = None

    @property
    def map(self):
        if not self._map:
            self._map = self.map_function()
        return self._map

    @map.setter
    def map(self, func):
        self._map = func

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

    @abstractmethod
    def __mul__(self, m: Union[Particle, 'TransferMap', Twiss]) -> Union[Particle, 'TransferMap', Twiss]:
        """[summary]
        A Transfermap can be multiplied by Particle, Twiss parameter or by a other TransferMap.
        :param m: a Particle, Twiss or TransferMap
        :type m: Particle, Twiss, TransferMap
        :return: a new Particle, Twiss or TransferMap 
        :rtype: TransferMap, 'TransferMap', Twiss
        """
        pass

    @abstractmethod
    def __call__(self, delta_length: float) -> 'TransferMap':
        """[summary]
        :param delta_length: delta length of the element
        :type delta_length: float        
        :return: a new TransferMap for delta_length
        :rtype: 'TransferMap'
        """
        pass
