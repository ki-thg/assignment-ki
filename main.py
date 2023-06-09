import sys

from src.main.billing_system.billing import BillingSystem
from src.main.fileio.reader import read_zone_map, read_journey_data
from src.main.fileio.writer import write_billing_results
from src.main.models.user import User


def main(zone_map_file, journey_data_file, output_file):
    zone_map = read_zone_map(zone_map_file)
    journey_data = read_journey_data(journey_data_file)
    billing_system = BillingSystem(zone_map)
    users = {}

    for user_id, station, direction, time in journey_data:
        if user_id not in users:
            users[user_id] = User(user_id)
        user = users[user_id]
        if direction == 'IN':
            if user.last_direction != "IN":
                user.enter_station(station, time)
            else:
                user.enter_station(station, time)
                user.exit_station(None, None)
        elif direction == 'OUT':
            if user.last_direction != "OUT":
                user.exit_station(station, time)
            else:
                user.exit_station(station, time)
                user.enter_station(None, None)

    for user in users.values():
        billing_system.calculate_charge(user)

    write_billing_results(output_file, users)


if __name__ == '__main__':
    zone_map_file = sys.argv[1]
    journey_data_file = sys.argv[2]
    output_file = sys.argv[3]
    main(zone_map_file, journey_data_file, output_file)
