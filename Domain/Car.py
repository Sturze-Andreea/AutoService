from Domain.Entity import Entity


class Car(Entity):
    """
    Car business object
    """

    def __init__(self, carId, model, acquisitionYear, kmNr, inGuarantee):
        """
        Creates a car
        :param carId: int, the car id
        :param model: string, the model
        :param acquisitionYear: int, the acquisition year
        :param kmNr: float, the number of kilometers
        :param inGuarantee: True if the car is in guarantee and False if not
        """
        super(Car, self).__init__(carId)
        self.__model = model
        self.__acquisitionYear = acquisitionYear
        self.__kmNr = kmNr
        self.__inGuarantee = inGuarantee

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, newModel):
        self.__model = newModel

    @property
    def acquisitionYear(self):
        return self.__acquisitionYear

    @acquisitionYear.setter
    def acquisitionYear(self, newAcqYear):
        self.__acquisitionYear = newAcqYear

    @property
    def kmNr(self):
        return self.__kmNr

    @kmNr.setter
    def kmNr(self, newKmNr):
        self.__kmNr = newKmNr

    @property
    def inGuarantee(self):
        return self.__inGuarantee

    @inGuarantee.setter
    def inGuarantee(self, newInGuarantee):
        self.__inGuarantee = newInGuarantee

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.entityId == other.entityId and self.model == other.model and \
            self.acquisitionYear == other.acquisitionYear and self.kmNr == other.kmNr and \
            self.inGuarantee == other.inGuarantee

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.entityId) + ", " + self.model + ", " + str(self.acquisitionYear) + ", " + \
               str(self.kmNr) + ", " + str(self.inGuarantee)
