import numpy as np


from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.tm_params.first_order_params import FirstOrderParams
from ocelot.cpbd.tm_params.second_order_params import SecondOrderParams
from ocelot.cpbd.high_order import fringe_ent, fringe_ext


class BendAtom(Element):
    """
    bending magnet
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    k1 - strength of quadrupole lens in [1/m^2],
    k2 - strength of sextupole lens in [1/m^3],
    tilt - tilt of lens in [rad],
    e1 - the angle of inclination of the entrance face [rad],
    e2 - the angle of inclination of the exit face [rad].
    fint - fringe field integral
    fintx - allows (fintx > 0) to set fint at the element exit different from its entry value.
    gap - the magnet gap [m], NOTE in MAD and ELEGANT: HGAP = gap/2
    h_pole1 - the curvature (1/r) of the entrance face
    h_pole1 - the curvature (1/r) of the exit face
    """

    def __init__(self, l=0., angle=0., k1=0., k2=0., e1=0., e2=0., tilt=0.0,
                 gap=0., h_pole1=0., h_pole2=0., fint=0., fintx=None, eid=None):
        super().__init__(eid=eid, has_edge=True)
        self.l = l
        self.angle = angle
        self.k1 = k1
        self.k2 = k2
        self.e1 = e1
        self.e2 = e2
        self.gap = gap
        self.h_pole1 = h_pole1
        self.h_pole2 = h_pole2
        self.fint = fint
        self.fintx = fint
        if fintx is not None:
            self.fintx = fintx
        self.tilt = tilt

    def __str__(self):
        s = 'Bend : '
        s += 'id = ' + str(self.id) + '\n'
        s += 'l       =%8.4f m\n' % self.l
        s += 'angle   =%8.3f deg\n' % (self.angle * 180.0 / np.pi)
        s += 'e1      =%8.3f deg\n' % (self.e1 * 180.0 / np.pi)
        s += 'e2      =%8.3f deg\n' % (self.e2 * 180.0 / np.pi)
        s += 'tilt    =%8.3f deg\n' % (self.tilt * 180.0 / np.pi)
        s += 'fint    =%8.3f\n' % self.fint
        s += 'fintx   =%8.3f\n' % self.fintx
        s += 'gap     =%8.4f m\n' % self.gap
        s += 'h_pole1 =%8.4f 1/m\n' % self.h_pole1
        s += 'h_pole2 =%8.4f 1/m\n' % self.h_pole2
        return s

    def _R_edge(self, fint, edge):
        if self.l != 0.:
            self.h = self.angle / self.l
        else:
            self.h = 0
        sec_e = 1. / np.cos(edge)
        phi = fint * self.h * self.gap * sec_e * (1. + np.sin(edge) ** 2)
        R = np.eye(6)
        R[1, 0] = self.h * np.tan(edge)
        R[3, 2] = -self.h * np.tan(edge - phi)
        return R

    def create_first_order_entrance_params(self, energy: float, delta_length: float = 0.0) -> FirstOrderParams:
        R = self._R_edge(self.fint, self.e1)
        B = self._default_B(R)
        return FirstOrderParams(R, B)

    def create_first_order_exit_params(self, energy: float, delta_length: float = 0.0) -> FirstOrderParams:
        R = self._R_edge(self.fintx, self.e2)
        B = self._default_B(R)
        return FirstOrderParams(R, B)

    def create_second_order_entrance_params(self, energy: float, delta_length: float = 0.0) -> SecondOrderParams:
        first_order_params = self.create_first_order_entrance_params(energy)
        _, T = fringe_ent(h=self.h, k1=self.k1, e=self.e1, h_pole=self.h_pole1,
                          gap=self.gap, fint=self.fint)
        return SecondOrderParams(first_order_params.R, first_order_params.B, T)

    def create_second_order_exit_params(self, energy: float, delta_length: float = 0.0) -> SecondOrderParams:
        first_order_params = self.create_first_order_exit_params(energy)
        _, T = fringe_ext(h=self.h, k1=self.k1, e=self.e2, h_pole=self.h_pole2,
                          gap=self.gap, fint=self.fintx)
        return SecondOrderParams(first_order_params.R, first_order_params.B, T)
