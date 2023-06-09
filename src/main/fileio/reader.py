import csv

def read_zone_map(zone_map_file):
    zone_map = {}
    try:
        with open(zone_map_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station = row['station']
                zone = int(row['zone'])
                zone_map[station] = zone
    except FileNotFoundError:
        print(f"The file {zone_map_file} does not exist.")
    except PermissionError:
        print(f"Lack of permission to read the file {zone_map_file}.")
    except csv.Error:
        print(f"There was a problem reading the file {zone_map_file}. It might not be a correctly formatted CSV file.")
    return zone_map


def read_journey_data(journey_data_file):
    journeys = []
    try:
        with open(journey_data_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row['user_id']
                station = row['station']
                direction = row['direction']
                time = row['time']
                journeys.append((user_id, station, direction, time))
    except FileNotFoundError:
        print(f"The file {journey_data_file} does not exist.")
    except PermissionError:
        print(f"Lack of permission to read the file {journey_data_file}.")
    except csv.Error:
        print(f"There was a problem reading the file {journey_data_file}. It might not be a correctly formatted CSV file.")
    return journeys
