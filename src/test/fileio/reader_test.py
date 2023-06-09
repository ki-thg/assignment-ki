import csv
import os

import pytest

from src.main.fileio.reader import read_zone_map, read_journey_data


@pytest.fixture(scope='module')
def test_zone_map_file():
    # Create test zone_map csv file
    file_path = 'test_zone_map.csv'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["station", "zone"])
        writer.writerow(["station_A", "1"])
        writer.writerow(["station_B", "2"])
        writer.writerow(["station_C", "3"])
        writer.writerow(["station_D", "2"])
    yield file_path
    # Remove test zone_map csv file
    os.remove(file_path)


@pytest.fixture(scope='module')
def test_journey_data_file():
    # Create test journey_data csv file
    file_path = 'test_journey_data.csv'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "station", "direction", "time"])
        writer.writerow(["user1", "station_A", "IN", "2023-01-01T9:40:00"])
        writer.writerow(["user2", "station_B", "IN", "2023-01-01T9:50:00"])
    yield file_path
    # Remove test journey_data csv file
    os.remove(file_path)


@pytest.fixture(scope='module')
def bad_zone_map_file():
    # Create faulty zone_map csv file
    file_path = 'bad_zone_map.csv'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["station"])  # missing "zone" column
        writer.writerow(["station_E"])
        writer.writerow(["station_F"])
        writer.writerow(["station_G"])
        writer.writerow(["station_H"])
    yield file_path
    # Remove faulty zone_map csv file
    os.remove(file_path)


@pytest.fixture(scope='module')
def bad_journey_data_file():
    file_path = 'bad_journey_data.csv'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "station"])
        writer.writerow(["user3", "station_E"])
        writer.writerow(["user4", "station_F"])
    yield file_path
    os.remove(file_path)


def test_read_zone_map(test_zone_map_file):
    # given a zone_map file exists
    # when I read from that file
    zone_map = read_zone_map(test_zone_map_file)
    # then retrieve the zone_map data as expected
    expected_zone_map = {
        "station_A": 1,
        "station_B": 2,
        "station_C": 3,
        "station_D": 2
    }
    assert zone_map == expected_zone_map


def test_read_journey_data(test_journey_data_file):
    # given a journey_data file exists
    # when I read from that file
    journey_data = read_journey_data(test_journey_data_file)
    # then retrieve the zone_map data as expected
    expected_journey_data = [
        ("user1", "station_A", "IN", "2023-01-01T9:40:00"),
        ("user2", "station_B", "IN", "2023-01-01T9:50:00"),
    ]
    assert journey_data == expected_journey_data


def test_bad_read_zone_map(bad_zone_map_file):
    # given an invalid zone_map file exists
    # when I read from that file then a KeyError exception is raised
    with pytest.raises(KeyError):
        read_zone_map(bad_zone_map_file)


def test_bad_read_journey_data(bad_journey_data_file):
    # given an invalid journey_data file exists
    # when I read from that file then a KeyError exception is raised
    with pytest.raises(KeyError):
        read_journey_data(bad_journey_data_file)
