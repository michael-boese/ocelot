from typing import List, Dict, Type

from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.transformations.transformation import Transformation, TMTypes


class OpticElement:
    """[summary]
    Facade between old interface an new interface.
    """

    def __init__(self, element: Element, tm: Type[Transformation]) -> None:
        self.__dict__['element'] = element
        self.__dict__['_tm_class_type'] = tm
        self.__dict__['_tms'] = self._create_tms(self.element, tm)

    # To access all getter attributes of element
    def __getattr__(self, name):
        if name in self.element.__dict__:
            return getattr(self.element, name)
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")

    # To access all setter attributes of element
    def __setattr__(self, name, value):
        if name in self.element.__dict__:
            return setattr(self.element, name, value)
        return object.__setattr__(self, name, value)

    @property
    def tms(self):
        return self._tms

    def R(self, energy):
        return [tm.get_params(energy).R for tm in self._tms]

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
            self._tm_class_type = tm
            self._tms = self._create_tms(self.element, tm)

    @staticmethod
    def _create_tms(element: Element, tm: Type[Transformation]) -> Dict[TMTypes, Type[Transformation]]:
        tms = []

        tms.append(tm.create(element, TMTypes.MAIN))
        if element.has_edge:
            tms.append(tm.create(element, TMTypes.ENTRANCE))
            tms.append(tm.create(element, TMTypes.EXIT))
        return tms

    @classmethod
    def create(cls, element: Element, tm: Type[Transformation]):
        return OpticElement(element=element, tm=tm)

    def __str__(self):
        return self.element.__str__()