import numpy as np

from ocelot.cpbd.transformations.v_corrector import VCorrectorTM
from ocelot.cpbd.elements.optic_element import OpticElement
from ocelot.cpbd.elements.vcor_atom import VcorAtom
from ocelot.cpbd.transformations.transfer_map import TransferMap


class Vcor(OpticElement):
    """
    horizontal corrector,
    l - length of magnet in [m],
    angle - angle of bend in [rad],
    """
    def __init__(self, l=0., angle=0., eid=None, tm=TransferMap):
        super().__init__(VcorAtom(l=l, angle=angle, eid=eid), tm=tm, default_tm=TransferMap)
