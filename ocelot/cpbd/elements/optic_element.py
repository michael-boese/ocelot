from copy import copy
from typing import List, Dict, Type


import numpy as np

from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.transformations import second_order
from ocelot.cpbd.transformations.transformation import Transformation, TMTypes
from ocelot.cpbd.transformations.second_order import SecondTM


class OpticElement:
    """[summary]
    Facade between old interface an new interface.
    """

    __is_init = False  # needed to disable __getattr__ and __setattr__ until __init__ is executed

    def __init__(self, element: Element, tm: Type[Transformation], default_tm: Transformation) -> None:
        self.element = element
        self.default_tm = default_tm
        self._first_order_tms = self._create_tms(self.element, default_tm)  # every optics element has a first_order tm to calculate e.g Twiss Paramters
        if default_tm == tm:
            self._tms = self._first_order_tms
            self._tm_class_type = tm
        else:
            self.__init_tms(tm)
        self.__is_init = True  # needed to disable __getattr__ and __setattr__ in __init__ phase

        # self.__dict__['element'] = element
        # self.__dict__['_tm_class_type'] = tm
        # self.__dict__['_tms'] = self._create_tms(self.element, tm)

    # To access all getter attributes of element
    def __getattr__(self, name):
        if self.__is_init and name in self.element.__dict__:
            return getattr(self.element, name)
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")

    # To access all setter attributes of element
    def __setattr__(self, name, value):
        if self.__is_init and name in self.element.__dict__:
            # TODO: If a element attribute is set, tm have to be recalculated. That means reset the cashed values in tms
            for tm in self._tms:
                tm._clean_cashed_values()
            return setattr(self.element, name, value)
        return object.__setattr__(self, name, value)

    @property
    def tms(self):
        return self._tms

    def B(self, energy):
        if self._tm_class_type == SecondTM:
            return [tm.get_params(energy).B for tm in self._tms]
        else:
            return [tm.get_params(energy).B for tm in self._first_order_tms]

    def R(self, energy):
        if self._tm_class_type == SecondTM:
            return [tm.get_params(energy).get_rotated_R() for tm in self._tms]
        else:
            return [tm.get_params(energy).get_rotated_R() for tm in self._first_order_tms]

    def T(self, energy):
        if self._tm_class_type == SecondTM:
            return [tm.get_params(energy).get_roteted_T() for tm in self._tms]
        else:
            return [np.zeros((6, 6, 6)) for _ in self._first_order_tms]

    def __init_tms(self, tm):
        try:
            self._tms = self._create_tms(self.element, tm)
            self._tm_class_type = tm
        except AttributeError as e:
            print(f"Can't set {tm.__name__} for {self.__class__.__name__} fall back to default tm which is {self.default_tm.__name__}.")
            self._tms = self._create_tms(self.element, self.default_tm)
            self._tm_class_type = self.default_tm

    def dot_tms(self, obj):
        """[summary]
        Multiplies all transforamtions with the object 
        :param obj: Object with which the transformations are be multiplied.
        :type obj: Twiss, Particle, ParticleArray
        :return: Deplends on the input type of obj.
        :rtype: Twiss, Particle, ParticleArray
        """
        new_obj = self._tms[0] * obj
        if len(self._tms) == 1:
            return new_obj
        else:
            for tm in self._tms[1:]:
                new_obj = tm * new_obj
            return new_obj

    def apply(self, X, energy):
        for tm in self._tms:
            tm.map_function(X, energy)

    def set_tm(self, tm: Transformation):
        if tm != self._tm_class_type:
            if tm == self.default_tm:
                self._tms = self._first_order_tms
            else:
                self.__init_tms(tm)

    def get_section_tms(self, delta_l: float, start_l: float = 0.0):
        #tms = [TMTypes.ROT_ENTRANCE]
        tm_list = []
        total_length = self.element.l
        if start_l < 1e-10:
            if self.element.has_edge:
                tm = self.get_tm(TMTypes.ENTRANCE)
                tm_list.append(copy(tm))
            if np.isclose(delta_l, total_length):
                tm = self.get_tm(TMTypes.MAIN)
                tm_list.append(copy(tm))
                if self.element.has_edge:
                    tm = self.get_tm(TMTypes.EXIT)
                    tm_list.append(copy(tm))
                return tm_list

        if (start_l + delta_l > total_length or np.isclose(start_l + delta_l, total_length)):
            delta_l_red = total_length - start_l
            TM_Class = self.get_tm(TMTypes.MAIN).__class__
            tm_list.append(TM_Class.from_element(element=self.element, tm_type=TMTypes.MAIN, delta_l=delta_l_red))
            if self.element.has_edge:
                tm = self.get_tm(TMTypes.EXIT)
                tm_list.append(copy(tm))
        else:
            TM_Class = self.get_tm(TMTypes.MAIN).__class__
            tm_list.append(TM_Class.from_element(element=self.element, tm_type=TMTypes.MAIN, delta_l=delta_l))
        # tms.append(TMTypes.ROT_EXIT)
        return tm_list

    def get_tm(self, tm_type: TMTypes):
        for tm in self._tms:
            if tm.tm_type == tm_type:
                return tm

    @staticmethod
    def _create_tms(element: Element, tm: Type[Transformation]) -> Dict[TMTypes, Type[Transformation]]:
        tms = []
        #tms = [tm.create(element, TMTypes.ROT_ENTRANCE)]
        if element.has_edge:
            tms.append(tm.from_element(element, TMTypes.ENTRANCE))
            tms.append(tm.from_element(element, TMTypes.MAIN))
            tms.append(tm.from_element(element, TMTypes.EXIT))
        else:
            tms.append(tm.from_element(element, TMTypes.MAIN))
        #tms = [tm.create(element, TMTypes.ROT_EXIT)]
        return tms

    @classmethod
    def create(cls, element: Element, tm: Type[Transformation]):
        return OpticElement(element=element, tm=tm)

    def __str__(self):
        return self.element.__str__()
