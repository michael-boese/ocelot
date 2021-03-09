import numpy as np

from ocelot.cpbd.tm_params.first_order_params import FirstOrderParams
from ocelot.cpbd.high_order import m_e_GeV
from ocelot.cpbd.elements.element import Element


class SolenoidAtom(Element):
    """
    Solenoid
    l - length in m,
    k - strength B0/(2B*rho)
    """

    def __init__(self, l=0., k=0., eid=None):
        Element.__init__(self, eid)
        self.k = k  # B0/(2B*rho)
        self.l = l

    def __str__(self):
        s = 'Cavity : '
        s += 'id = ' + str(self.id) + '\n'
        s += 'l =%8.4f m\n' % self.l
        s += 'k =%8.3f 1/m\n' % self.k
        return s

    def create_first_order_main_params(self, energy: float, delta_length: float) -> FirstOrderParams:
        R = self.R_main_matrix(energy=energy, length=delta_length if delta_length != 0.0 else self.l)
        B = self._default_B(R)
        return FirstOrderParams(R, B, self.tilt)

    def R_main_matrix(self, energy, length):

        def sol(l, k, energy):
            """
            K.Brown, A.Chao.
            :param l: effective length of solenoid
            :param k: B0/(2*Brho), B0 is field inside the solenoid, Brho is momentum of central trajectory
            :return: matrix
            """
            gamma = energy / m_e_GeV
            c = np.cos(l * k)
            s = np.sin(l * k)
            if k == 0:
                s_k = l
            else:
                s_k = s / k
            r56 = 0.
            if gamma != 0:
                gamma2 = gamma * gamma
                beta = np.sqrt(1. - 1. / gamma2)
                r56 -= l / (beta * beta * gamma2)
            sol_matrix = np.array([[c * c, c * s_k, s * c, s * s_k, 0., 0.],
                                   [-k * s * c, c * c, -k * s * s, s * c, 0., 0.],
                                   [-s * c, -s * s_k, c * c, c * s_k, 0., 0.],
                                   [k * s * s, -s * c, -k * s * c, c * c, 0., 0.],
                                   [0., 0., 0., 0., 1., r56],
                                   [0., 0., 0., 0., 0., 1.]]).real
            return sol_matrix

        return sol(length, k=self.k, energy=energy)
