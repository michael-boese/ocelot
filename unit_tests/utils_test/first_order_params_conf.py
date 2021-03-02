"""Test parameters description file"""

import pytest
import json
import os


class Data():
    def __init__(self, ground_truth_data):
        self.ground_truth_data = ground_truth_data

    def get_R(self, element_name: str):
        return self.ground_truth_data[element_name]['R']

    def get_B(self, element_name: str):
        return self.ground_truth_data[element_name]['B']

    def get_energy(self, element_name: str):
        return self.ground_truth_data[element_name]['energy_list']

    def zip(self, element_name: str):
        return zip(self.get_energy(element_name), self.get_R(element_name), self.get_B(element_name))


@pytest.fixture(scope='module')
def load_ground_truth_data():
    cwd = os.getcwd()
    with open('unit_tests/test_data/first_oder_param_ground_truth.json') as fp:
        ground_truth_data = json.load(fp)
    return Data(ground_truth_data)