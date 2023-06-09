from datetime import datetime


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.entered_stations = []
        self.exited_stations = []
        self.entered_times = []
        self.exited_times = []
        self.last_direction = None
        self.charge = 0.0

    def __str__(self):
        return f"User(user_id={self.user_id}, entered_stations={self.entered_stations}, exited_stations={self.exited_stations}, entered_times={self.entered_times}, exited_times={self.exited_times}, charge={self.charge})"

    def enter_station(self, station, time):
        if station == None:
            self.entered_stations.append(None)
            self.entered_times.append(None)
        else:
            self.entered_stations.append(station)
            timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            self.entered_times.append(timestamp)
            self.last_direction = "IN"

    def exit_station(self, station, time):
        if station == None:
            self.exited_stations.append(None)
            self.exited_times.append(None)
        else:
            self.exited_stations.append(station)
            timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            self.exited_times.append(timestamp)
            self.last_direction = "OUT"
