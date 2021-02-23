from ocelot.cpbd.transformations.params.tm_params import TMParams

class FirstOrderParams(TMParams):
    def __init__(self, R, B) -> None:
        super().__init__()
        self.R = R
        self.B = B
