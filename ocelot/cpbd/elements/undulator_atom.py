import numpy as np

from ocelot.cpbd.high_order import m_e_GeV
from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.field_map import FieldMap
from ocelot.cpbd.tm_params.first_order_params import FirstOrderParams


class UndulatorAtom(Element):
    """
    Undulator
    lperiod - undulator period in [m];\n
    nperiod - number of periods;\n
    Kx - undulator paramenter for vertical field; \n
    Ky - undulator parameter for horizantal field;\n
    field_file - absolute path to magnetic field data;\n
    mag_field - None by default, the magnetic field map function - (Bx, By, Bz) = f(x, y, z)
    eid - id of undulator.
    """

    def __init__(self, lperiod=0., nperiods=0, Kx=0., Ky=0., field_file=None, eid=None):
        Element.__init__(self, eid)
        self.lperiod = lperiod
        self.nperiods = nperiods
        self.l = lperiod * nperiods
        self.Kx = Kx
        self.Ky = Ky
        self.solver = "linear"  # can be "lin" is linear matrix,  "sym" - symplectic method and "rk" is Runge-Kutta
        self.phase = 0.  # phase between Bx and By + pi/4 (spiral undulator)

        self.ax = -1  # width of undulator, when ax is negative undulator width is infinite
        # I need this for analytic description of undulator

        self.field_file = field_file
        self.field_map = FieldMap(self.field_file)
        self.mag_field = None  # the magnetic field map function - (Bx, By, Bz) = f(x, y, z)
        self.v_angle = 0.
        self.h_angle = 0.

    def __str__(self):
        s = 'Undulator : '
        s += 'id = ' + str(self.id) + '\n'
        s += 'l        =%8.4f m\n' % self.l
        s += 'nperiods =%8.1f \n' % self.nperiods
        s += 'lperiod  =%8.4f m\n' % self.lperiod
        s += 'Kx       =%8.3f \n' % self.Kx
        s += 'Ky       =%8.3f \n' % self.Ky
        return s

    def create_first_order_main_params(self, energy: float, delta_length: float) -> FirstOrderParams:
        R = self.R_main_matrix(energy=energy, length=delta_length if delta_length != 0.0 else self.l)
        B = self._default_B(R)
        return FirstOrderParams(R, B, self.tilt)

    def R_main_matrix(self, energy, length):
        """
        in OCELOT coordinates:
        R56 = - Lu/(gamma**2 * beta**2) * (1 + 0.5 * K**2 * beta**2)
        S.Tomin, Varenna, 2017.
        """

        def undulator_r_z(z, lperiod, Kx, Ky, energy):
            gamma = energy / m_e_GeV
            r = np.eye(6)
            r[0, 1] = z
            if gamma != 0 and lperiod != 0 and Kx != 0:
                beta = 1 / np.sqrt(1.0 - 1.0 / (gamma * gamma))

                omega_x = np.sqrt(2.0) * np.pi * Kx / (lperiod * gamma * beta)
                omega_y = np.sqrt(2.0) * np.pi * Ky / (lperiod * gamma * beta)
                r[2, 2] = np.cos(omega_x * z)
                r[2, 3] = np.sin(omega_x * z) / omega_x
                r[3, 2] = -np.sin(omega_x * z) * omega_x
                r[3, 3] = np.cos(omega_x * z)

                r[4, 5] = - z / (gamma * beta) ** 2 * (1 + 0.5 * (Kx * beta) ** 2)

            else:
                r[2, 3] = z
            return r

        R = undulator_r_z(length, lperiod=self.lperiod, Kx=self.Kx, Ky=self.Ky, energy=energy)
        return R
