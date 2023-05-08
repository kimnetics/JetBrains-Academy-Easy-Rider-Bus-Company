class Line:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.start_id = None
        self.start_name = None
        self.finish_name = None
        self.stops = {}

        self.validation_errors = []

    def add_stop(self, stop):
        # Process stop type.
        if stop.stop_type == 'S':
            if self.start_name is not None:
                self.validation_errors.append('More than one start.')

            self.start_id = stop.stop_id
            self.start_name = stop.stop_name
        elif stop.stop_type == 'O':
            pass
        elif stop.stop_type == 'F':
            if self.finish_name is not None:
                self.validation_errors.append('More than one finish.')

            self.finish_name = stop.stop_name

        # Add stop to dictionary.
        self.stops[stop.stop_id] = stop

    def get_arrival_error(self):
        # Return error if no start.
        if self.start_id is None:
            return f'bus_id line {self.bus_id}: missing start'

        # Assuming arrival times do not go into next day.

        arrival_time = '00:00'
        stop = self.stops[self.start_id]
        while stop is not None:
            if stop.a_time is None or stop.a_time <= arrival_time:
                return f'bus_id line {stop.bus_id}: wrong time on station {stop.stop_name}'

            if stop.next_stop is None or stop.stop_type == 'F':
                stop = None
            else:
                if stop.next_stop not in self.stops:
                    return f'bus_id line {stop.bus_id}: wrong next stop on station {stop.stop_name}'

                arrival_time = stop.a_time
                stop = self.stops[stop.next_stop]

        return None
