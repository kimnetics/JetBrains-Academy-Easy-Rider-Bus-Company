# JetBrains Academy Easy Rider Bus Company Project

An example of a passing solution to the final phase of the JetBrains Academy Python Easy Rider Bus Company project.

## Description

This project is a command line application which validates and/or summarizes incoming bus schedule data.

Bus schedule data is input in a JSON string.

The project went through six stages with each stage validating and/or summarizing different areas of the bus schedule data structure.

## Notes

The relative directory structure was kept the same as the one used in my JetBrains Academy solution.

The application is started by running `easyrider.py`.

### Validation Logic

In addition to the other validation logic present, the `Stop` class has generalized field validation logic configured with a structure like the following:

```
    FIELDS = {
        'bus_id': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_id': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_name': {'type': str, 'required': True,
                      'regex': re.compile(r'[A-Z][\w\s.]+(Road|Avenue|Boulevard|Street)')},
        'next_stop': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_type': {'type': str, 'required': False, 'regex': re.compile(r'[SOF]?')},
        'a_time': {'type': str, 'required': True, 'regex': re.compile(r'([0-1][0-9]|2[0-3]):[0-5][0-9]')}
    }
```

Fields are checked for data type, being required and format.

### Saving / Loading Data

The requirements could be vague at times. To allow replaying of incoming bus schedule data for debugging, I added an easy way to save and load bus schedule data. This is done via a config file (`config.json`) which looks like the following:

```
{
  "json_file_path": "/Users/me/Temp/easyrider",
  "fixed_data_number": 0,
  "save_schedule": true
}
```

The config file is used as follows:

1. Set `json_file_path` to the directory you would like to save schedule data to.

2. Set `fixed_data_number` to 0 to indicate schedule data should be input versus read from a prior save file.

3. Set `save_schedule` to true to save incoming schedule data.

4. Check your solution with JetBrains Academy.

5. You will now have a file named `schedule.json` in your directory.

6. Add an '_' + number to the end of `schedule.json`. For example: `schedule_1.json`.

7. Set `fixed_data_number` to the number you used.

8. You can now run the application in dev mode using the saved data. Adjust the logic until you get the desired application behavior.

9. Set `fixed_data_number` back to 0 to allow the application to go back to receiving incoming schedule data.

### Example Bus Schedule

Here is an example bus schedule JSON string:

```
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
```
