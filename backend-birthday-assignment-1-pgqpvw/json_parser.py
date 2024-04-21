import json
from datetime import datetime
import jsonschema
from jsonschema import Draft202012Validator as Validator


class JsonParser:
    SCHEMA = {
        "type": "array",
        "prefixItems": [
            {"name": "Last Name", "type": "string"},
            {"name": "First Name", "type": "string"},
            {"name": "DOB", "type": "datetime"},
        ],
    }

    def __init__(self, input_file):
        self.input_file = input_file

    def call(self):
        try:
            with open(self.input_file) as file:
                json_data = json.load(file)
                output = []
                for entry in json_data:
                    entry = self._transform_and_validate(entry)
                    if entry is not False:
                        output.append(entry)
                    else:
                        continue

            print(f"JSON parsed succesfully. {len(output)} birthdays imported")
            return output
        except json.decoder.JSONDecodeError:
            print("JSON file could not be loaded, please check format is correct.")
            return []

    def _transform_and_validate(self, entry):
        try:
            entry[2] = self._transform_date(entry[2])
            self._validate_json_schema(entry)
            return tuple(entry)
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False

    def _transform_date(self, date):
        try:
            return datetime.strptime(date, "%Y/%m/%d")
        except (ValueError, TypeError):
            return date

    def _validate_json_schema(self, entry):
        v = Validator

        def is_datetime(_checker, inst):
            return isinstance(inst, datetime)

        date_check = v.TYPE_CHECKER.redefine("datetime", is_datetime)
        v = jsonschema.validators.extend(v, type_checker=date_check)
        v(schema=self.SCHEMA).validate(entry)
