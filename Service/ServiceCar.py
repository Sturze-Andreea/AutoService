import datetime
import random

from Domain.Car import Car


class ServiceCar:
    """
    Manages car logic
    """
    def __init__(self, repository, validator, repositoryTransaction, undoList, redoList):
        """
        Creates a car service
        :param repository: RepositoryCar
        :param validator: CarValidator
        """
        self.__repository = repository
        self.__validator = validator
        self.__repositoryTransaction = repositoryTransaction
        self.__undoList = undoList
        self.__redoList = redoList

    def addCar(self, id, model, year, km, guarantee):
        """
        Creates a car
        :param id: int, the id
        :param model: str, the model
        :param year: int, the year
        :param km: float, the number of kilometers
        :param guarantee: bool, if the car is in guarantee
        """
        car = Car(id, model, year, km, guarantee)
        self.__validator.validate(car)
        self.__repository.create(car)
        self.__undoList.append([lambda: self.__repository.delete(car.entityId), lambda: self.__repository.create(car)])
        self.__redoList.clear()

    def getAll(self):
        """
        :return: a list of all cars
        """
        return self.__repository.read()

    def deleteCar(self, id):
        """
        Deletes a car
        :param id: int, the id
        """
        list = []
        car = self.__repository.read(id)
        for transaction in self.__repositoryTransaction.read():
            if transaction.carId == id:
                list.append(transaction)
                self.__repositoryTransaction.delete(transaction.entityId)
        self.__repository.delete(id)
        list.append([lambda: self.__repository.create(car), lambda: self.__repository.delete(id)])
        self.__undoList.append(list)
        self.__redoList.clear()

    def updateCar(self, id, model, year, km, guarantee):
        """
        Updates a car
        :param id: int, the id
        :param model: str, the model
        :param year: int, the year
        :param km: float, the nr of km
        :param guarantee: bool
        """
        car1 = self.__repository.read(id)
        car = Car(id, model, year, km, guarantee)
        self.__validator.validate(car)
        self.__repository.update(car)
        self.__undoList.append([lambda: self.__repository.update(car1), lambda: self.__repository.update(car)])
        self.__redoList.clear()

    def getCar(self, id):
        """
        :param id: int
        :return: a car
        """
        return self.__repository.read(id)

    @staticmethod
    def randomModel():
        """
        Gets a random model
        :return: the model
        """
        return random.choice(["Dacia", "Ferrari", "Audi", "Bmw", "Tesla", "Seat"])

    @staticmethod
    def randomYear():
        """
        Gets a random year
        :return: the year
        """
        return random.choice([2010, 2011, 2012, 2013, 2014, 2003, 2009, 2007, 2018, 2017])

    @staticmethod
    def randomKm():
        """
        Gets a random number of km
        :return: the nr of km
        """
        return random.choice([1234.5, 4567.8, 64280.0, 98673.8, 46843.8, 28464.5, 56835.5])

    @staticmethod
    def randomGuarantee():
        """
        Gets a random guarantee
        :return: the guarantee
        """
        return random.choice([True, False])

    def randomCars(self, n):
        """
        Creates a number random cars
        :param n: the given number
        """
        list = []
        ind = 0
        if self.__repository.read():
            ind = max([self.__repository.read()[i].entityId for i in range(len(self.__repository.read()))])
        for index in range(n):
            ind = ind + 1
            car = Car(ind, self.randomModel(), int(self.randomYear()), float(self.randomKm()), self.randomGuarantee())
            self.__repository.create(car)
            list.append(ind)
        self.__undoList.append(list)
        self.__redoList.clear()

    def updateGuarantee(self):
        """
        Updates the guarantee for every car
        """
        list = []
        for car in self.__repository.read():
            if car.kmNr - 60000 > 0 or datetime.datetime.now().year - car.acquisitionYear > 3:
                list.append(car)
                car1 = Car(car.entityId, car.model, car.acquisitionYear, car.kmNr, False)
                self.__repository.update(car1)
        self.__undoList.append(list)

    def searchByModel(self, model):
        """
        Searches the cars by model
        :param model: string
        :return: the list of cars
        """
        list = self.__repository.read()
        return filter(lambda car: car.model == model, list)

    def searchByYear(self, year):
        """
        Searches the cars by year
        :param year: int
        :return: the list of cars
        """
        list = self.__repository.read()
        return filter(lambda car: car.acquisitionYear == year, list)

    def searchByKm(self, km):
        """
        Searches the cars by km nr
        :param km: float
        :return: the list of cars
        """
        list = self.__repository.read()
        return filter(lambda car: car.kmNr == km, list)
