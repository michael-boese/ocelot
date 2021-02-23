from typing import List, Dict, Type

from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.transformations.transformation import Transformation, TMTypes

class OpticElement:
    """[summary]
    Facade between old interface an new interface.
    """

    def __init__(self, element: Element, tm: Type[Transformation]) -> None:
        self.element = element
        self._class_type_tms = self._set_class_type_tms(element, tm)
        self._tms: List[Transformation] = []
        self._energy = None

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, energy):
        if not self._energy or self._energy != energy:
            self._tms = self.calculate_tms(energy)
            self._energy = energy

    def tms(self, energy):
        self.energy = energy
        return self._tms

    def R(self, energy):
        self.energy = energy
        return [tm.params.R for tm in self._tms]

    def calculate_tms(self, energy):
        return [tm_cls(element=self.element, tm_type=tm_type, energy=energy) for tm_type, tm_cls in self._class_type_tms.items()]

    def apply(self, X, energy):
        self.energy = energy
        for tm in self._tms:
            tm.map_function(X, energy)

    def set_tm(self, tm: Transformation):
        self._class_type_tms = self._set_class_type_tms(self.element, tm)
        self._energy = None

    @staticmethod
    def _set_class_type_tms(element: Element, tm: Type[Transformation]) -> Dict[TMTypes, Type[Transformation]]:
        tms = []
        tms = {TMTypes.MAIN: tm}
        if element.has_edge:
            tms[TMTypes.ENTRANCE] = tm
            tms[TMTypes.EXIT] = tm
        return tms

    @classmethod
    def create(cls, element: Element, tm: Type[Transformation]):
        return OpticElement(element=element, tm=tm)

    def __str__(self):
        return self.element.__str__()
