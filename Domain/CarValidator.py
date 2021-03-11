import datetime


class CarValidationError(Exception):
    pass


class CarValidator:

    @staticmethod
    def validate(car):
        errors = []
        if type(car.entityId) != int:
            errors.append("The id should be integer!")
        if type(car.acquisitionYear) != int or 1750 > car.acquisitionYear or car.acquisitionYear > \
                datetime.datetime.now().year:
            errors.append("The year must be integer and between 1750 and the current year!")
        if type(car.kmNr) != float or car.kmNr < 0:
            errors.append("The number of kilometers should be rational and positive!")
        if car.inGuarantee not in [True, False]:
            errors.append("The in guarantee should be either True or False!")
        if errors:
            raise CarValidationError(errors)
