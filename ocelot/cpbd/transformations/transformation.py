import enum
from copy import deepcopy, copy
import functools
import logging
from sys import flags
from typing import Callable, Union
from abc import ABC, abstractmethod

from ocelot.cpbd.beam import Twiss, Particle, ParticleArray

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

    def __init__(self, create_tm_param_func, delta_e_func, tm_type: TMTypes, length: float, delta_length: float = 0.0) -> None:
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

        self._map = None

    def get_delta_e(self):
        if self._delta_e_func:
            return self._delta_e_func(delta_length=self.delta_length, total_length=self.length)
        else:
            return 0.0

    @classmethod
    def create(cls, main_tm_params_func, delta_e_func, length, delta_length=0.0, entrance_tm_params_func=None, exit_tm_params_func=None, tm_type: TMTypes = TMTypes.MAIN):
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
        if delta_length > length:
            _logger.warning("delta_l > length of element. Set delta_l == length of element.")
            delta_length = length
        return cls(create_tm_param_func=tm_params_func, delta_e_func=delta_e_func, tm_type=tm_type, length=length, delta_length=delta_length)

    # twiss and tms using the same parameter
    # @functools.lru_cache(maxsize=3)
    def get_params(self, energy: float):
        return self.create_tm_param_func(energy, self.delta_length)

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

    # @abstractmethod
    # def __call__(self, delta_length: float) -> 'TransferMap':
    #     """[summary]
    #     :param delta_length: delta length of the element
    #     :type delta_length: float
    #     :return: a new TransferMap for delta_length
    #     :rtype: 'TransferMap'
    #     """
    #     pass
