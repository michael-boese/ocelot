from ocelot.cpbd.transformations.params.first_order_params import FirstOrderParams

class SecondOrderParams(FirstOrderParams):
    def __init__(self, R, B, T) -> None:
        super().__init__()
        self.R = R
        self.B = B
        self.T = T