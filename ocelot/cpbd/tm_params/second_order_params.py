from ocelot.cpbd.tm_params.first_order_params import FirstOrderParams


class SecondOrderParams(FirstOrderParams):
    def __init__(self, R, B, T) -> None:
        super().__init__(R, B)
        self.T = T
