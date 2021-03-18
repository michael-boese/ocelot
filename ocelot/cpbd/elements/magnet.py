from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.tm_params.kick_params import KickParams

class Magnet(Element):
    def __init__(self, eid=None, has_edge=False):
        super().__init__(eid=None, has_edge=False)
        self.angle = 0. # Magnets Drift, Bend, Correctors (just angle)
        self.k1 = 0. # Magnets quatropole
        self.k2 = 0. # Magnets Sixtropole

    def create_kick_entrance_params(self) -> KickParams:
        return KickParams(dx=self.dx, dy=self.dy, angle=self.angle, tilt=self.tilt, k1=self.k1, k2=self.k2)

    def create_kick_main_params(self) -> KickParams:
        return KickParams(dx=self.dx, dy=self.dy, angle=self.angle, tilt=self.tilt, k1=self.k1, k2=self.k2)

    def create_kick_exit_params(self) -> KickParams:
        return KickParams(dx=self.dx, dy=self.dy, angle=self.angle, tilt=self.tilt, k1=self.k1, k2=self.k2)