import datetime
import calendar


class Person:
    def __init__(self, last_name, first_name, dob):
        self.last_name = last_name
        self.first_name = first_name
        self.dob = dob

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def isbirthday(self):
        today = datetime.date.today()

        if self.dob.month == 2 and self.dob.day == 29:
            return self._handle_leap_year_births()
        else:
            return bool(today.month == self.dob.month and today.day == self.dob.day)

    def _handle_leap_year_births(self):
        today = datetime.date.today()

        if calendar.isleap(today.year):
            return bool(today.month == 2 and today.day == 29)
        else:
            return bool(today.month == 2 and today.day == 28)
