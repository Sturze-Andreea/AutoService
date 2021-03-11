import datetime

from Domain.Car import Car
from Domain.Exceptions import NoObjectError
from Domain.Transaction import Transaction
from Domain.TransactionView import TransactionView


class ServiceTransaction:
    """
    Manages transaction logic
    """
    def __init__(self, transactionRepository, carRepository, cardRepository, validator, undoList, redoList):
        """
        Creates a transaction service
        :param transactionRepository: RepositoryTransaction
        :param carRepository: RepositoryCar
        :param cardRepository: RepositoryCard
        :param validator: TransactionValidator
        """
        self.__transactionRepository = transactionRepository
        self.__carRepository = carRepository
        self.__cardRepository = cardRepository
        self.__validator = validator
        self.__undoList = undoList
        self.__redoList = redoList

    def addTransaction(self, id, carId, cardId, pieces, workmanship, dateAndHour):
        """
        Creates a transaction
        :param id: int
        :param carId: int
        :param cardId: int
        :param pieces: float, price
        :param workmanship: float, price
        :param dateAndHour: str, dd.mm.yyyy
        """
        if self.__carRepository.read(carId) is None:
            raise NoObjectError("There is no car with this id!")
        if self.__cardRepository.read(cardId) is None and cardId != 0:
            raise NoObjectError("There is no card with this id!")
        transaction = Transaction(id, carId, cardId, pieces, workmanship, dateAndHour)
        self.__validator.validate(transaction)
        self.__transactionRepository.create(transaction)
        self.applyDiscounts(id)
        self.__undoList.append([lambda: self.__transactionRepository.delete(id),
                                lambda: self.__transactionRepository.create(self.__transactionRepository.read(id))])
        self.__redoList.clear()

    def getTransactions(self):
        """
        :return: a list of all transactions
        """
        return self.__transactionRepository.read()

    def getAll(self):
        """
        :return: a list of all transactions views
        """
        transactions = self.__transactionRepository.read()
        return map(lambda transaction: TransactionView(transaction, self.__carRepository.read(transaction.carId),
                                        self.__cardRepository.read(transaction.cardId)), transactions)

    def deleteTransaction(self, id):
        """
        Deletes a transaction
        :param id: int
        """
        t = self.__transactionRepository.read(id)
        self.__transactionRepository.delete(id)
        self.__undoList.append([lambda: self.__transactionRepository.create(t),
                                lambda: self.__transactionRepository.delete(id)])
        self.__redoList.clear()

    def updateTransaction(self, id, carId, cardId, pieces, workmanship, dateAndHour):
        """
        Updates a transaction
        :param id: int
        :param carId: int
        :param cardId: int
        :param pieces: float,price
        :param workmanship: float, price
        :param dateAndHour: str, dd.mm.yyyy
        :return:
        """
        if self.__carRepository.read(carId) is None:
            raise NoObjectError("There is no car with this id!")
        if self.__cardRepository.read(cardId) is None and cardId != 0:
            raise NoObjectError("There is no card with this id!")
        t1 = self.__transactionRepository.read(id)
        transaction = Transaction(id, carId, cardId, pieces, workmanship, dateAndHour)
        self.__validator.validate(transaction)
        self.__transactionRepository.update(transaction)
        self.__undoList.append([lambda: self.__transactionRepository.update(t1),
                                lambda: self.__transactionRepository.update(transaction)])
        self.__redoList.clear()

    def applyDiscountPieces(self, id):
        """
        Applies the discount for pieces
        :param id: int
        """
        transaction = self.__transactionRepository.read(id)
        if transaction is None:
            raise NoObjectError("No transaction with the given id exists!")
        if transaction.cardId != 0:
            newWork = transaction.workmanship - 0.1 * transaction.workmanship
            transaction1 = Transaction(transaction.entityId, transaction.carId, transaction.cardId,
                                       transaction.pieces, newWork, transaction.dateAndHour,
                                       transaction.discountPieces, 0.1 * transaction.workmanship)
            self.__transactionRepository.update(transaction1)

    def applyDiscountWorkmanship(self, id):
        """
        Applies discount for workmanship
        :param id: the id, int
        """
        transaction = self.__transactionRepository.read(id)
        if transaction is None:
            raise NoObjectError("No transaction with the given id exists!")
        if self.__carRepository.read(transaction.carId).inGuarantee:
            transaction2 = Transaction(transaction.entityId, transaction.carId, transaction.cardId,
                                       0, transaction.workmanship, transaction.dateAndHour, transaction.pieces,
                                       transaction.discountWorkmanship)
            self.__transactionRepository.update(transaction2)

    def applyDiscounts(self, id):
        """
        Applies the discounts
        :param id: int
        """
        self.applyDiscountPieces(id)
        self.applyDiscountWorkmanship(id)

    def deleteTransactionsFromDays(self, day1, day2):
        """
        Deletes transactions from an interval of days
        :param day1: first day
        :param day2: second day
        """
        list = []
        x = day1.split(".")
        try:
            int(x[0])
            int(x[1])
            int(x[2])
            day1 = datetime.date(int(x[2]), int(x[1]), int(x[0]))
        except ValueError:
            raise ValueError("Wrong date")
        y = day2.split(".")
        try:
            int(y[0])
            int(y[1])
            int(y[2])
            day2 = datetime.date(int(y[2]), int(y[1]), int(y[0]))
        except ValueError:
            raise ValueError("Wrong date")
        for transaction in self.__transactionRepository.read():
            date = transaction.dateAndHour
            z = date.split(" ")
            a = z[0].split(".")
            date = datetime.date(int(a[2]), int(a[1]), int(a[0]))
            if day1 <= date <= day2:
                list.append(transaction)
                self.__transactionRepository.delete(transaction.entityId)
        self.__undoList.append(list)

    def sortTransactionsByWorkmanship(self):
        """
        Sorts transactions by workmanship price
        :return: a list of sorted transactions
        """
        sort = self.mySort(self.__transactionRepository.read(), key=lambda transaction1: transaction1.workmanship,
                      reverse=True)
        return sort

    def sortCarsByWorkmanshipRecursive(self, list):
        """
        Sorts cars by workmanship price
        :return: a list of sorted cars
        """
        if not list:
            return []
        return [self.__carRepository.read(list[0].carId)] + self.sortCarsByWorkmanshipRecursive(list[1:])

    def sortCarsByWorkmanship(self):
        """
        Sorts cars by workmanship price
        :return: a list of sorted cars
        """
        return self.sortCarsByWorkmanshipRecursive(self.sortTransactionsByWorkmanship())

    def findTransactionsBetweenSums(self, sum1, sum2):
        """
        Finds transactions with sum between two given sums
        :param sum1: the first sum ,float
        :param sum2:  the second sum, float
        :return: a list of transactions
        """
        list = self.__transactionRepository.read()
        return filter(lambda transaction: sum1 < transaction.workmanship + transaction.pieces < sum2, list)

    def sortCardsByDiscounts(self):
        """
        Sorts cards by discount
        :return: the list of sorted cards
        """
        sort = self.mySort(self.__transactionRepository.read(), key=lambda transaction1: transaction1.
                                    discountWorkmanship + transaction1.discountPieces, reverse=True)
        return map(lambda transaction: self.__cardRepository.read(transaction.cardId), sort)

    def doUndo(self):
        """
        Undo function
        """
        if len(self.__undoList) > 0:
            op = self.__undoList.pop()
            if isinstance(op[0], int):
                l = []
                while op:
                    o = op[-1]
                    l.append(self.__carRepository.read(o))
                    self.__carRepository.delete(o)
                    del op[-1]
                self.__redoList.append(l)
            elif isinstance(op[0], Car):
                l = []
                for i in range(len(op)-1, -1, -1):
                    l.append(self.__carRepository.read(op[i].entityId))
                    self.__carRepository.update(op[i])
                l.append("update")
                self.__redoList.append(l)
            elif isinstance(op[0], Transaction):
                if isinstance(op[-1], list):
                    l = []
                    for i in range(len(op) - 2, -1, -1):
                        l.append(op[i].entityId)
                        self.__transactionRepository.create(op[i])
                    l.append([op[len(op)-1][1], op[len(op)-1][0]])
                    op[len(op) - 1][0]()
                    self.__redoList.append(l)
                else:
                    l = []
                    for i in range(len(op) - 1, -1, -1):
                        l.append(op[i].entityId)
                        self.__transactionRepository.create(op[i])
                    self.__redoList.append(l)
            else:
                self.__redoList.append([op[1], op[0]])
                op[0]()

    def doRedo(self):
        """
        Redo function
        :return:
        """
        if len(self.__redoList) > 0:
            op = self.__redoList.pop()
            if isinstance(op[0], Car):
                if isinstance(op[-1], str):
                    l = []
                    for i in range(len(op) - 2, -1, -1):
                        l.append(self.__carRepository.read(op[i].entityId))
                        self.__carRepository.update(op[i])
                    self.__undoList.append(l)
                else:
                    l = []
                    for i in range(len(op)-1, -1, -1):
                        l.append(op[i].entityId)
                        self.__carRepository.create(op[i])
                    self.__undoList.append(l)
            elif isinstance(op[0], int):
                if isinstance(op[-1], list):
                    l = []
                    lst = [op[len(op) - 1][1], op[len(op) - 1][0]]
                    op[len(op) - 1][0]()
                    del op[-1]
                    while op:
                        o = op[-1]
                        l.append(self.__transactionRepository.read(o))
                        self.__transactionRepository.delete(o)
                        del op[-1]
                    l.append(lst)
                    self.__undoList.append(l)
                else:
                    l = []
                    while op:
                        o = op[-1]
                        l.append(self.__transactionRepository.read(o))
                        self.__transactionRepository.delete(o)
                        del op[-1]
                    self.__undoList.append(l)
            else:
                self.__undoList.append([op[1], op[0]])
                op[0]()

    @staticmethod
    def mySort(list, key=None, reverse=False):
        """
        Selection sort
        :param list: a list
        :param key: the key
        :param reverse: bool
        :return: the list of sorted elements
        """
        newList = list[:]
        for index in range(len(newList)):
            for index2 in range(index+1, len(newList)):
                elem1 = newList[index]
                elem2 = newList[index2]
                if key is not None:
                    elem1 = key(elem1)
                    elem2 = key(elem2)
                cond = elem1 > elem2
                if reverse is True:
                    cond = not cond
                if cond:
                    newList[index], newList[index2] = newList[index2], newList[index]
        return newList
