from Domain.CarValidator import CarValidator
from Domain.CardValidator import CardValidator
from Domain.TransactionValidator import TransactionValidator
from Repository.GenericFileRepository import GenericFileRepository
from Service.ServiceCar import ServiceCar
from Service.ServiceCard import ServiceCard
from Service.ServiceTransaction import ServiceTransaction
from UserInterface.Console import Console


def main():
    undoList = []
    redoList = []
    carRepository = GenericFileRepository("cars.pkl")
    cardRepository = GenericFileRepository("cards.pkl")
    transactionRepository = GenericFileRepository("transactions.pkl")
    carValidator = CarValidator()
    cardValidator = CardValidator(cardRepository)
    transactionValidator = TransactionValidator()
    carService = ServiceCar(carRepository, carValidator, transactionRepository, undoList, redoList)
    cardService = ServiceCard(cardRepository, cardValidator, transactionRepository, undoList, redoList)
    transactionService = ServiceTransaction(transactionRepository, carRepository, cardRepository, transactionValidator,
                                            undoList, redoList)
    console = Console(carService, cardService, transactionService)
    console.runConsole()


main()
