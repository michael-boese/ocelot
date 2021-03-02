import numpy as np
from ocelot.cpbd.tm_params.tm_params import TMParams


class FirstOrderParams(TMParams):
    def __init__(self, R, B) -> None:
        super().__init__()
        self.R = R
        self.B = B

    def multiply(self, tm_params: 'FirstOrderParams'):
        R = np.dot(self.R, tm_params.R)
        B = np.dot(self.R, tm_params.B) + self.B
        return FirstOrderParams(R, B)