from itertools import zip_longest


class BillingSystem:
    def __init__(self, zone_map):
        self.zone_map = zone_map
        self.zone_prices = {
            1: 0.80,
            2: 0.50,
            3: 0.50,
            4: 0.30,
            5: 0.30,
            6: 0.10
        }
        self.monthly_cap = 100.00
        self.daily_cap = 15.00

    def calculate_charge(self, user):

        daily_charge, monthly_total, total = 0.00, 0.00, 0.00
        previous_month, previous_day, current_month, current_day = None, None, None, None

        for entry_station, entry_timestamp, exit_station, exit_timestamp in zip_longest(user.entered_stations,
                                                                                        user.entered_times,
                                                                                        user.exited_stations,
                                                                                        user.exited_times):
            entry_zone = self.zone_map.get(entry_station)
            exit_zone = self.zone_map.get(exit_station)

            if entry_timestamp is not None:
                current_month = entry_timestamp.month
                current_day = entry_timestamp.day
            elif exit_timestamp is not None:
                current_month = exit_timestamp.month
                current_day = exit_timestamp.day

            if current_day != previous_day:
                previous_day = current_day
                monthly_total += min(daily_charge, 15.00)
                daily_charge = 0.00
                if current_month != previous_month:
                    previous_month = current_month
                    total += min(monthly_total, 100.00)
                    monthly_total = 0.00

            if entry_zone is None or exit_zone is None:
                daily_charge += 5.00
            else:
                journey_charge = self.calculate_journey_charge(entry_zone, exit_zone)
                daily_charge += journey_charge

        if monthly_total + min(daily_charge, 15.00) < 100.00:
            total += monthly_total + min(daily_charge, 15.00)
        else:
            total += 100.00
        user.charge = round(total, 2)

    def calculate_journey_charge(self, entry_zone, exit_zone):
        if entry_zone == exit_zone:
            additional_cost = 2.00 * self.zone_prices[entry_zone]
        else:
            additional_cost = self.zone_prices[entry_zone] + self.zone_prices[exit_zone]
        journey_charge = 2.00 + additional_cost
        return journey_charge
