class BirthdayDeterminer:
    def __init__(self):
        pass

    def call(self, list_of_people):
        birthday_people = [person for person in list_of_people if person.isbirthday()]
        if birthday_people:
            print("Today's birthdays are:")
            for person in birthday_people:
                print(person)
        else:
            print("There are no birthdays today.")

        return birthday_people
