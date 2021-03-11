from Domain.Card import Card
from Domain.Exceptions import DuplicateCNPError


class ServiceCard:
    """
    Manages card logic
    """
    def __init__(self, repository, validator, repositoryTransaction, undoList, redoList):
        """
        Creates a card service
        :param repository: RepositoryCard
        :param validator: CardValidator
        """
        self.__repository = repository
        self.__validator = validator
        self.__repositoryTransaction = repositoryTransaction
        self.__undoList = undoList
        self.__redoList = redoList

    def addCard(self, id, lastName, firstName, CNP, birthDate, regDate):
        """
        Creates a card
        :param id: int
        :param lastName: str
        :param firstName: str
        :param CNP: int, 13 digits
        :param birthDate: str, dd.mm.yyyy
        :param regDate: str, dd.mm.yyyy
        """
        for c in self.__repository.read():
            if c.CNP == CNP:
                raise DuplicateCNPError("The CNP already exists in a card!")
        card = Card(id, lastName, firstName, CNP, birthDate, regDate)
        self.__validator.validate(card)
        self.__repository.create(card)
        self.__undoList.append([lambda: self.__repository.delete(id), lambda: self.__repository.create(card)])
        self.__redoList.clear()

    def getAll(self):
        """
        :return: a list of all cards
        """
        return self.__repository.read()

    def deleteCard(self, id):
        """
        Deletes a card
        :param id: int
        """
        list = []
        card = self.__repository.read(id)
        for transaction in self.__repositoryTransaction.read():
            if transaction.cardId == id:
                list.append(transaction)
                self.__repositoryTransaction.delete(transaction.entityId)
        self.__repository.delete(id)
        list.append([lambda: self.__repository.create(card), lambda: self.__repository.delete(id)])
        self.__undoList.append(list)
        self.__redoList.clear()

    def updateCard(self, id, lastName, firstName, CNP, birthDate, regDate):
        """
        Updates a card
        :param id: int
        :param lastName: str
        :param firstName: str
        :param CNP: int, 13 digits
        :param birthDate: str, dd.mm.yyyy
        :param regDate: str, dd.mm.yyyy
        """
        card1 = self.__repository.read(id)
        card = Card(id, lastName, firstName, CNP, birthDate, regDate)
        self.__validator.validate(card)
        self.__repository.update(card)
        self.__undoList.append([lambda: self.__repository.update(card1), lambda: self.__repository.update(card)])
        self.__redoList.clear()

    def getCard(self, id):
        """
        :param id: int
        :return: a card
        """
        return self.__repository.read(id)

    def searchByLastName(self, name):
        """
        Searches the cards by last name
        :param name: str
        :return: a list of cards
        """
        list = self.__repository.read()
        return filter(lambda card: card.lastName == name, list)

    def searchByFirstName(self, name):
        """
        Searches the cards by first name
        :param name: str
        :return: a list of cards
        """
        list = self.__repository.read()
        return filter(lambda card: card.firstName == name, list)

    def searchByCNP(self, CNP):
        """
        Searches the cards by CNP
        :param CNP: int
        :return: a list of cards
        """
        list = self.__repository.read()
        return filter(lambda card: card.CNP == CNP, list)

    def searchByBirthDate(self, date):
        """
        Searches the cards by birth date
        :param date: str, dd.mm.yyyy
        :return: a list of cards
        """
        list = self.__repository.read()
        return filter(lambda card: card.birthDate == date, list)

    def searchByRegistrationDate(self, date):
        """
        Searches the cards by registration date
        :param date: str, dd.mm.yyyy
        :return: a list of cards
        """
        list = self.__repository.read()
        return filter(lambda card: card.registrationDate == date, list)

    def permutations(self):
        results = []
        crtPermut = self.__repository.read()
        n = len(crtPermut)

        def inner(crtPerm):
            if len(crtPerm) == n:
                results.append(crtPerm)
                return

            for i in range(n):
                if crtPermut[i] not in crtPerm:
                    inner(crtPerm + [crtPermut[i]])

        inner([])
        return results
