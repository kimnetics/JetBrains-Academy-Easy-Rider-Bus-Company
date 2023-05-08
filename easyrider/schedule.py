import json
import os

from line import Line
from stop import Stop


class Schedule:
    def __init__(self, config):
        # Set location of schedule data json files.
        self.json_file_path = config['json_file_path']

        # Determine where to get schedule data.
        fixed_data_number = config['fixed_data_number']
        if fixed_data_number:
            self.__use_saved_data(fixed_data_number)
        else:
            input_json = input()
            self.schedule_data = json.loads(input_json)

        # If configured, save schedule data.
        if config['save_schedule']:
            self.__save_schedule()

        # Prepare stop data.
        self.stops = []
        self.stops_usage = {}
        self.__prepare_stops()

        # Prepare line data.
        self.lines = {}
        self.__prepare_lines()

    def __prepare_stops(self):
        # Loop through schedule.
        for stop_fields in self.schedule_data:
            self.stops.append(Stop(stop_fields))

        # Loop through stops.
        for stop in self.stops:
            if stop.stop_name in self.stops_usage:
                self.stops_usage[stop.stop_name].append(stop.bus_id)
            else:
                self.stops_usage[stop.stop_name] = [stop.bus_id]

    def __prepare_lines(self):
        # Loop through stops.
        for stop in self.stops:
            # If not present, add line.
            if stop.bus_id not in self.lines:
                self.lines[stop.bus_id] = Line(stop.bus_id)

            # Add stop to line.
            self.lines[stop.bus_id].add_stop(stop)

    def print_stop_summary(self):
        start_names = []
        finish_names = []
        transfer_names = []
        self.__get_stop_summary(start_names, finish_names, transfer_names)

        print(f'Start stops: {len(start_names)} {start_names}')
        print(f'Transfer stops: {len(transfer_names)} {transfer_names}')
        print(f'Finish stops: {len(finish_names)} {finish_names}')

    def __get_stop_summary(self, start_names, finish_names, transfer_names):
        start_dictionary = {}
        finish_dictionary = {}

        # Loop through lines.
        for bus_id, line in self.lines.items():
            if line.start_name is None or line.finish_name is None:
                print(f'There is no start or end stop for the line: {line.bus_id}.')
                return

            if len(line.validation_errors) > 0:
                print(f'There is more than one start or end stop for the line: {line.bus_id}.')
                return

            # Add start and finish stops.
            if line.start_name is not None:
                start_dictionary[line.start_name] = None
            if line.finish_name is not None:
                finish_dictionary[line.finish_name] = None

        start_names.extend(list(start_dictionary.keys()))
        finish_names.extend(list(finish_dictionary.keys()))

        for stop_name, bus_ids in self.stops_usage.items():
            # Add transfer stops.
            if stop_name is not None and len(bus_ids) > 1:
                transfer_names.append(stop_name)

        start_names.sort()
        finish_names.sort()
        transfer_names.sort()

    def print_arrival_errors(self):
        errors = []

        # Loop through lines.
        for bus_id, line in self.lines.items():
            error = line.get_arrival_error()
            if error is not None:
                errors.append(error)

        print('Arrival time test:')
        if len(errors) == 0:
            print('OK')
        else:
            for error in errors:
                print(error)

    def print_on_demand_errors(self):
        start_names = []
        finish_names = []
        transfer_names = []
        self.__get_stop_summary(start_names, finish_names, transfer_names)

        # Make dictionary of special stops.
        special_names = {}
        special_names.update(dict.fromkeys(start_names, None))
        special_names.update(dict.fromkeys(finish_names, None))
        special_names.update(dict.fromkeys(transfer_names, None))

        on_demand_error_stops = []
        # Loop through stops.
        for stop in self.stops:
            if stop.stop_type == 'O' and stop.stop_name in special_names:
                on_demand_error_stops.append(stop.stop_name)
        on_demand_error_stops.sort()

        print('On demand stops test:')
        if len(on_demand_error_stops) == 0:
            print('OK')
        else:
            print(f'Wrong stop type: {on_demand_error_stops}')

    def __use_saved_data(self, number):
        file_name = f'{self.json_file_path}/schedule_{number}.json'
        if not os.path.exists(file_name):
            print(f'File {file_name} not found.')
            return

        # Read schedule from file.
        with open(file_name, 'r') as file:
            self.schedule_data = json.load(file)

    def __save_schedule(self):
        schedule_json = json.dumps(self.schedule_data)

        # Write schedule to file.
        file_name = f'{self.json_file_path}/schedule.json'
        with open(file_name, 'w') as file:
            file.write(schedule_json)
