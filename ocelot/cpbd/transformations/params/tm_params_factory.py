from ocelot.cpbd.transformations.params.first_order_params import FirstOrderParams
from ocelot.cpbd.transformations.params.second_order_params import SecondOrderParams


class TMParamsFactory:
    """[summary]
    Defines all factory methods that each element can implement. Notes, that each 
    element have to implement the factory method for the first order.
    Raises:
        NotImplementedError: If a function is not implemented by an element.
    """

    def __not_impl_error_message(self, func_name: str) -> str:
        return f"class {self.__class__.__name__} have to implement {func_name}."
    
    # First Order
    def create_first_order_main_params(self, energy: float, delta_length: float) -> FirstOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_first_order_main_params.__name__))

    def create_first_order_entrance_params(self, energy: float, delta_length: float) -> FirstOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_first_order_entrance_params.__name__))

    def create_first_order_exit_params(self, energy: float, delta_length: float) -> FirstOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_first_order_exit_params.__name__))

    # Second Order
    def create_second_order_main_params(self, energy: float, delta_length: float) -> SecondOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_second_order_main_params.__name__))

    def create_second_order_entrance_params(self, energy: float, delta_length: float) -> SecondOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_second_order_entrance_params.__name__))

    def create_second_order_exit_params(self, energy: float, delta_length: float) -> SecondOrderParams:
        raise NotImplementedError(self.__not_impl_error_message(self.create_second_order_exit_params.__name__))
