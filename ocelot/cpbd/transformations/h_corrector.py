from ocelot.cpbd.high_order import t_nnn
from ocelot.cpbd.tm_utils import SecondOrderMult
from ocelot.cpbd.transformations.corrector import CorrectorTM


class HCorrectorTM(CorrectorTM):
    @classmethod
    def create_from_element(cls, element, params=None):
        def t_mat_z_e(z, energy): return t_nnn(z, 0, 0, 0, energy)
        tm = cls(angle_x=element.angle, angle_y=0., r_z_no_tilt=element.create_r_matrix(), t_mat_z_e=t_mat_z_e)
        tm.multiplication = SecondOrderMult().tmat_multip
        return tm
