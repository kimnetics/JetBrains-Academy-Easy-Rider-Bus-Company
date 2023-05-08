import json
import os

from schedule import Schedule


def main():
    config = __read_config()

    schedule = Schedule(config)
    schedule.print_on_demand_errors()


def __read_config():
    # Config file relative location varies between running in dev mode and test mode.
    file_name = 'config.json'
    if not os.path.exists(file_name):
        file_name = '../config.json'

    with open(file_name, 'r') as file:
        return json.load(file)


if __name__ == "__main__":
    main()
