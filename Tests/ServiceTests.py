from math import fabs

from Domain.Car import Car
from Domain.CarValidator import CarValidator
from Domain.Card import Card
from Domain.CardValidator import CardValidator
from Domain.Exceptions import RepositoryError, DuplicateCNPError
from Domain.Transaction import Transaction
from Domain.TransactionValidator import TransactionValidator
from Repository.GenericFileRepository import GenericFileRepository
from Service.ServiceCar import ServiceCar
from Service.ServiceCard import ServiceCard
from Service.ServiceTransaction import ServiceTransaction

EPSILON = 0.001


def test_car_service():
    undoList = []
    redoList = []
    carValidator = CarValidator()
    transactionRepository = GenericFileRepository("testTransactions.pkl")
    carRepository = GenericFileRepository("testCars.pkl")
    carRepository.clear()
    carService = ServiceCar(carRepository, carValidator, transactionRepository, undoList, redoList)
    car = Car(1, "Logan", 2010, 2345.7, True)
    carService.addCar(car.entityId, car.model, car.acquisitionYear, car.kmNr, car.inGuarantee)
    assert carService.getAll() == [car]
    try:
        carService.addCar(car.entityId, car.model, car.acquisitionYear, car.kmNr, car.inGuarantee)
        assert False
    except RepositoryError:
        assert True


test_car_service()


def test_card_service():
    undoList = []
    redoList = []
    transactionRepository = GenericFileRepository("testTransactions.pkl")
    cardRepository = GenericFileRepository("testCards.pkl")
    cardValidator = CardValidator(cardRepository)
    cardRepository.clear()
    cardService = ServiceCard(cardRepository, cardValidator, transactionRepository, undoList, redoList)
    card = Card(1, "Pop", "Ion", 1960412123456, "12.04.1996", "21.10.2018")
    cardService.addCard(card.entityId, card.lastName, card.firstName, card.CNP, card.birthDate, card.registrationDate)
    assert cardService.getAll() == [card]
    try:
        cardService.addCard(card.entityId, card.lastName, card.firstName, card.CNP, card.birthDate,
                            card.registrationDate)
        assert False
    except DuplicateCNPError:
        assert True


test_card_service()


def test_transaction_service():
    undoList = []
    redoList = []
    transactionValidator = TransactionValidator()
    cardRepository = GenericFileRepository("testCards.pkl")
    carRepository = GenericFileRepository("testCars.pkl")
    transactionRepository = GenericFileRepository("testTransactions.pkl")
    transactionRepository.clear()
    transactionService = ServiceTransaction(transactionRepository, carRepository, cardRepository, transactionValidator,
                                            undoList, redoList)
    transaction = Transaction(1, 1, 1, 100.0, 40.0, "21.10.2018 14:34")
    transactionService.addTransaction(transaction.entityId, transaction.carId, transaction.cardId, transaction.pieces,
                                      transaction.workmanship, transaction.dateAndHour)
    try:
        transactionService.addTransaction(transaction.entityId, transaction.carId, transaction.cardId,
                                          transaction.pieces, transaction.workmanship, transaction.dateAndHour)
        assert False
    except RepositoryError:
        assert True
    assert transactionService.getTransactions()[0].entityId == 1
    assert transactionService.getTransactions()[0].carId == 1
    assert transactionService.getTransactions()[0].cardId == 1
    assert fabs(transactionService.getTransactions()[0].pieces - 0.0) < EPSILON
    assert fabs(transactionService.getTransactions()[0].workmanship - 36.0) < EPSILON
    assert transactionService.getTransactions()[0].dateAndHour == "21.10.2018 14:34"
    assert transactionService.findTransactionsBetweenSums(130.0, 200.0) == []
    assert transactionService.findTransactionsBetweenSums(30.0, 100.0) == transactionService.getTransactions()
    transactionService.deleteTransactionsFromDays("12.10.2018", "20.03.2019")
    assert transactionService.getTransactions() == []


test_transaction_service()
