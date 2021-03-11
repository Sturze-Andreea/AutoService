import datetime


class TransactionValidationError(Exception):
    pass


class TransactionValidator:

    @staticmethod
    def validate(transaction):
        errors = []
        if type(transaction.entityId) != int:
            errors.append("The id should be integer!")
        if type(transaction.carId) != int:
            errors.append("The id should be integer!")
        if type(transaction.cardId) != int:
            errors.append("The id should be integer!")
        if type(transaction.pieces) != float:
            errors.append("The price for pieces should be rational!")
        if type(transaction.workmanship) != float:
            errors.append("The price for workmanship should be rational!")
        z = transaction.dateAndHour.split(" ")
        if len(z) != 2:
            errors.append("Date and hour should be (dd.mm.yyyy hh:mm)")
        else:
            x = z[0].split(".")
            if len(x) != 3:
                errors.append("Date should be (dd.mm.yyyy)")
            else:
                try:
                    int(x[0])
                    int(x[1])
                    int(x[2])
                except ValueError:
                    errors.append("Wrong date")
                if not 0 < int(x[0]) < 32:
                    errors.append("The day should be between 1 and 31!")
                if not 0 < int(x[1]) < 13:
                    errors.append("The month must be between 1 and 12!")
                if not int(x[2]) < datetime.datetime.now().year:
                    errors.append("The year must smaller than the current year!")
            y = z[1].split(":")
            if len(y) != 2:
                errors.append("Hour should be (hh:mm)")
            else:
                try:
                    int(y[0])
                    int(y[1])
                except ValueError:
                    errors.append("Wrong hour")
                if not 0 < int(y[0]) < 24:
                    errors.append("Hour must be between 0 and 24!")
                if not 0 < int(y[1]) < 60:
                    errors.append("Minute must be between 0 and 60!")
        if errors:
            raise TransactionValidationError(errors)
