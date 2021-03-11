from Domain.Entity import Entity


class Transaction(Entity):
    """
    Transaction business object
    """

    def __init__(self, id, carId, cardId, pieces, workmanship, dateAndHour, discountPieces=0, discountWorkmanship=0):
        """
        Creates a transaction
        :param id: int, the transaction id
        :param carId: int, the car id
        :param cardId: int, the card id
        :param pieces: float, the price for pieces
        :param workmanship: float, the price for workmanship
        :param dateAndHour: string, dd.mm.yyyy
        """
        super(Transaction, self).__init__(id)
        self.__carId = carId
        self.__cardId = cardId
        self.__pieces = pieces
        self.__workmanship = workmanship
        self.__dateAndHour = dateAndHour
        self.__discountPieces = discountPieces
        self.__discountWorkmanship = discountWorkmanship

    @property
    def carId(self):
        return self.__carId

    @carId.setter
    def carId(self, newCarId):
        self.__carId = newCarId

    @property
    def cardId(self):
        return self.__cardId

    @cardId.setter
    def cardId(self, newCardId):
        self.__cardId = newCardId

    @property
    def pieces(self):
        return self.__pieces

    @pieces.setter
    def pieces(self, newPieces):
        self.__pieces = newPieces

    @property
    def workmanship(self):
        return self.__workmanship

    @workmanship.setter
    def workmanship(self, newWorkmanship):
        self.__workmanship = newWorkmanship

    @property
    def dateAndHour(self):
        return self.__dateAndHour

    @dateAndHour.setter
    def dateAndHour(self, newDateAndHour):
        self.__dateAndHour = newDateAndHour

    @property
    def discountPieces(self):
        return self.__discountPieces

    @discountPieces.setter
    def discountPieces(self, newDisc):
        self.__discountPieces = newDisc

    @property
    def discountWorkmanship(self):
        return self.__discountWorkmanship

    @discountWorkmanship.setter
    def discountWorkmanship(self, newDisc):
        self.__discountWorkmanship = newDisc

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.entityId == other.entityId and self.carId == other.carId and \
            self.cardId == other.cardId and self.pieces == other.pieces and \
            self.workmanship == other.workmanship and self.dateAndHour == other.dateAndHour

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.entityId) + ", " + str(self.carId) + ", " + str(self.cardId) + ", " + str(self.pieces) + ", " +\
            str(self.workmanship) + ", " + self.dateAndHour
