from datetime import datetime, timedelta

import pytest

from src.main.billing_system.billing import BillingSystem
from src.main.models.user import User


@pytest.fixture
def billing_system():
    zone_map = {
        'think_tank_terminus': 1,
        'payments_junction': 2,
        'core_cross': 3,
        'cloud_lane': 2
    }
    return BillingSystem(zone_map)


def test_calculate_charge_single_journey(billing_system):
    # Given a user exists with a single complete journey
    user = User('user1')
    user.enter_station('think_tank_terminus', '2022-04-04T09:40:00')
    user.exit_station('core_cross', '2022-04-04T13:55:00')

    # when total cost for user is calculated
    billing_system.calculate_charge(user)

    # then correct total is returned
    assert user.charge == 3.3


def test_calculate_charge_erroneous_journey(billing_system):
    # Given a user exists with a journey that is incomplete
    user = User('user2')
    user.enter_station('think_tank_terminus', '2022-04-04T09:50:00')

    # when total cost for user is calculated
    billing_system.calculate_charge(user)

    # then £5 fee is returned
    assert user.charge == 5.0


def test_calculate_charge_daily_cap(billing_system):
    # Given a user exists with journeys that accumulate past the daily cap
    user = User('user3')
    user.enter_station('think_tank_terminus', '2022-04-05T11:30:00')
    user.exit_station('cloud_lane', '2022-04-05T12:02:11')
    user.enter_station('cloud_lane', '2022-04-05T13:44:07')
    user.exit_station('core_cross', '2022-04-05T14:30:37')
    user.enter_station('think_tank_terminus', '2022-04-05T15:14:12')
    user.exit_station('payments_junction', '2022-04-05T15:24:28')
    user.enter_station('payments_junction', '2022-04-05T20:14:52')
    user.exit_station('think_tank_terminus', '2022-04-05T21:42:00')
    user.enter_station('think_tank_terminus', '2022-04-05T22:10:00')
    user.exit_station('payments_junction', '2022-04-05T23:40:00')
    user.enter_station('payments_junction', '2022-04-06T05:10:00')
    user.exit_station('think_tank_terminus', '2022-04-06T07:40:00')

    # when total cost for user is calculated
    billing_system.calculate_charge(user)

    # then the daily cap is accounted for and correct total returned
    assert user.charge == 18.3


def test_calculate_charge_monthly_cap(billing_system):
    # Given a user exists that has journeys that accumulate past the £100 threshold, spanning across 8 days with 7 journeys per day
    user = User('user3')
    current_date = datetime(2022, 4, 1)
    for _ in range(8):
        current_time = current_date + timedelta(hours=11, minutes=30)
        for _ in range(7):
            user.enter_station('think_tank_terminus', current_time.strftime('%Y-%m-%dT%H:%M:%S'))

            current_time += timedelta(minutes=30)

            user.exit_station('cloud_lane', current_time.strftime('%Y-%m-%dT%H:%M:%S'))

            current_time += timedelta(minutes=1)

        current_date += timedelta(days=1)

    # when total cost for user is calculated
    billing_system.calculate_charge(user)

    # then total should be capped at £100
    assert user.charge == 100.0


def test_calculate_charge_across_multiple_months(billing_system):
    # Given a user exists with journeys that span across multiple months
    user = User('user3')
    user.enter_station('think_tank_terminus', '2022-04-05T11:30:00')
    user.exit_station('cloud_lane', '2022-04-05T12:02:11')
    user.enter_station('cloud_lane', '2022-05-05T13:44:07')
    user.exit_station('core_cross', '2022-05-05T14:30:37')
    user.enter_station('think_tank_terminus', '2022-05-05T15:14:12')
    user.exit_station('payments_junction', '2022-05-05T15:24:28')
    user.enter_station('think_tank_terminus', '2022-06-05T11:30:00')
    user.exit_station('cloud_lane', '2022-06-05T12:02:11')

    # when total cost for user is calculated
    billing_system.calculate_charge(user)

    # then the daily cap is accounted for and correct total returned
    assert user.charge == 12.90
