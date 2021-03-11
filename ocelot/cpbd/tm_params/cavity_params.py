import numpy as np
from ocelot.cpbd.tm_params.first_order_params import FirstOrderParams
from ocelot.cpbd.r_matrix import rot_mtx
import functools

class CavityParams(FirstOrderParams):
    def __init__(self, R, B, tilt) -> None:
        super().__init__(R, B, tilt)
        self.R = R
        self.B = B
        self.tilt = tilt
