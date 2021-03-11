import datetime


class CardValidationError(Exception):
    pass


class CardValidator:

    def __init__(self, repo):
        self.__repository = repo

    def validate(self, card):
        errors = []
        if type(card.entityId) != int:
            errors.append("The id should be integer!")
        if type(card.CNP) != int or len(str(card.CNP)) != 13:
            errors.append("The CNP should have 13 digits!")
        for c in self.__repository.read():
            if c.CNP == card.CNP:
                errors.append("Duplicate CNP!")
        x = card.birthDate.split(".")
        if len(x) != 3:
            errors.append("Wrong birth date")
        else:
            try:
                int(x[0])
                int(x[1])
                int(x[2])
            except ValueError:
                errors.append("Wrong birth date")
            if not 0 < int(x[0]) < 32:
                errors.append("The birth day should be between 1 and 31!")
            if not 0 < int(x[1]) < 13:
                errors.append("The birth month must be between 1 and 12!")
            if not int(x[2]) < datetime.datetime.now().year:
                errors.append("The birth year must smaller than the current year!")
        y = card.registrationDate.split(".")
        if len(y) != 3:
            errors.append("Wrong registration date")
        else:
            try:
                int(y[0])
                int(y[1])
                int(y[2])
            except ValueError:
                errors.append("Wrong registration date")
            if not 0 < int(y[0]) < 32:
                errors.append("The registration day should be between 1 and 31!")
            if not 0 < int(y[1]) < 13:
                errors.append("The registration month must be between 1 and 12!")
            if not int(y[2]) < datetime.datetime.now().year:
                errors.append("The registration year must smaller than the current year!")
        if errors:
            raise CardValidationError(errors)
