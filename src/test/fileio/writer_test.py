import csv
import os

import pytest

from src.main.fileio.writer import write_billing_results
from src.main.models.user import User


@pytest.fixture
def users():
    user1 = User('user1')
    user1.charge = 15.25

    user2 = User('user2')
    user2.charge = 10.00

    user3 = User('user3')
    user3.charge = 17.75

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3
    }


def teardown_module(module):
    # Remove test output file
    if os.path.exists('test_output.csv'):
        os.remove('test_output.csv')


def test_write_billing_results(users):
    # given users exist with associated charges
    # when I write the results to a file
    write_billing_results('test_output.csv', users)

    # then I expect file to have the correct results
    expected_output = [
        ['user1', 15.25],
        ['user2', 10.00],
        ['user3', 17.75]
    ]

    with open('test_output.csv', 'r') as file:
        reader = csv.reader(file)
        output = list(reader)

    expected_output = [[row[0], float(row[1])] for row in expected_output]
    output = [[row[0], float(row[1])] for row in output]

    assert output == expected_output
