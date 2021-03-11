from Domain.Entity import Entity


class Card(Entity):
    """
    Card business object
    """

    def __init__(self, cardId, lastName, firstName, CNP, birthDate, registrationDate):
        """
        Creates a card
        :param cardId: int, the card id
        :param lastName: string, the last name
        :param firstName: string, the first name
        :param CNP: int, the CNP, 13 digits
        :param birthDate: string, dd.mm.yyyy
        :param registrationDate: string, dd.mm.yyyy
        """
        super(Card, self).__init__(cardId)
        self.__lastName = lastName
        self.__firstName = firstName
        self.__CNP = CNP
        self.__birthDate = birthDate
        self.__registrationDate = registrationDate

    @property
    def lastName(self):
        return self.__lastName

    @lastName.setter
    def lastName(self, newLastName):
        self.__lastName = newLastName

    @property
    def firstName(self):
        return self.__firstName

    @firstName.setter
    def firstName(self, newFirstName):
        self.__firstName = newFirstName

    @property
    def CNP(self):
        return self.__CNP

    @CNP.setter
    def CNP(self, newCNP):
        self.__CNP = newCNP

    @property
    def birthDate(self):
        return self.__birthDate

    @birthDate.setter
    def birthDate(self, newBirthDate):
        self.__birthDate = newBirthDate

    @property
    def registrationDate(self):
        return self.__registrationDate

    @registrationDate.setter
    def registrationDate(self, newRegDate):
        self.__registrationDate = newRegDate

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.entityId == other.entityId and self.lastName == other.lastName and \
            self.firstName == other.firstName and self.CNP == other.CNP and \
            self.birthDate == other.birthDate and self.registrationDate == other.registrationDate

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.entityId) + ", " + self.lastName + ", " + self.firstName + ", " + str(self.CNP) + ", " + \
               self.birthDate + ", " + self.registrationDate
