import re


class Stop:
    FIELDS = {
        'bus_id': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_id': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_name': {'type': str, 'required': True,
                      'regex': re.compile(r'[A-Z][\w\s.]+(Road|Avenue|Boulevard|Street)')},
        'next_stop': {'type': int, 'required': True, 'regex': re.compile(r'\d+')},
        'stop_type': {'type': str, 'required': False, 'regex': re.compile(r'[SOF]?')},
        'a_time': {'type': str, 'required': True, 'regex': re.compile(r'([0-1][0-9]|2[0-3]):[0-5][0-9]')}
    }

    def __init__(self, fields):
        self.bus_id = None
        self.stop_id = None
        self.stop_name = None
        self.next_stop = None
        self.stop_type = None
        self.a_time = None

        self.validation_errors = []
        for field in Stop.FIELDS:
            if self.__field_is_valid(field, fields.get(field)):
                setattr(self, field, fields.get(field))

        self.unrecognized_fields = []
        for field in fields:
            if field not in Stop.FIELDS:
                self.unrecognized_fields.append(field)

    def __field_is_valid(self, field, value):
        rules = Stop.FIELDS.get(field)

        # Handle data type check.
        if value is not None:
            if not isinstance(value, rules['type']):
                self.validation_errors.append(field)
                return False

        # Handle required field check.
        if rules['required']:
            if value is None:
                self.validation_errors.append(field)
                return False

        # Handle regex check.
        if rules['regex']:
            if not rules['regex'].fullmatch(str(value)):
                self.validation_errors.append(field)
                return False

        return True

    def get_validation_errors(self):
        return self.validation_errors
