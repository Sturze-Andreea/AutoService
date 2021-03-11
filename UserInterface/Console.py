from Domain.CarValidator import CarValidationError
from Domain.CardValidator import CardValidationError
from Domain.TransactionValidator import TransactionValidationError


class Console:

    def __init__(self, carService, cardService, transactionService):
        self.__carService = carService
        self.__cardService = cardService
        self.__transactionService = transactionService

    @staticmethod
    def __showMenu():
        print(" ")
        print("1.Cars")
        print("2.Cards")
        print("3.Transactions")
        print("4.Others")
        print("5.Undo")
        print("6.Redo")
        print("x.Exit")
        print(" ")

    def runConsole(self):
        while True:
            self.__showMenu()
            op = input("Option: ")
            if op == "1":
                self.__menuCars()
            elif op == "2":
                self.__menuCards()
            elif op == "3":
                self.__menuTransactions()
            elif op == "4":
                self.__menuOthers()
            elif op == "5":
                self.__transactionService.doUndo()
            elif op == "6":
                self.__transactionService.doRedo()
            elif op == "x":
                break
            else:
                print("Invalid option!")

    @staticmethod
    def __showMenuCars():
        print(" ")
        print("---Cars---")
        print("1.Add")
        print("2.Delete")
        print("3.Update")
        print("4.Populate n")
        print("a.Show")
        print("b.Back")
        print(" ")

    def __menuCars(self):
        while True:
            self.__showMenuCars()
            op = input("Option: ")
            if op == "1":
                self.__handleAddCar()
            elif op == "2":
                self.__handleDeleteCar()
            elif op == "3":
                self.__handleUpdateCar()
            elif op == "4":
                self.__handleAddRandomCar()
            elif op == "a":
                self.__handleShowList(self.__carService.getAll())
            elif op == "b":
                break
            else:
                print("Invalid option!")

    @staticmethod
    def __showMenuCards():
        print(" ")
        print("---Cards---")
        print("1.Add")
        print("2.Delete")
        print("3.Update")
        print("4.Show all permutations")
        print("a.Show")
        print("b.Back")
        print(" ")

    def __menuCards(self):
        while True:
            self.__showMenuCards()
            op = input("Option: ")
            if op == "1":
                self.__handleAddCard()
            elif op == "2":
                self.__handleDeleteCard()
            elif op == "3":
                self.__handleUpdateCard()
            elif op == "4":
                self.__handleShowPermutations(self.__cardService.permutations())
            elif op == "a":
                self.__handleShowList(self.__cardService.getAll())
            elif op == "b":
                break
            else:
                print("Invalid option!")

    @staticmethod
    def __showMenuTransactions():
        print(" ")
        print("---Transactions---")
        print("1.Add")
        print("2.Delete")
        print("3.Update")
        print("a.Show")
        print("b.Back")
        print(" ")

    def __menuTransactions(self):
        while True:
            self.__showMenuTransactions()
            op = input("Option: ")
            if op == "1":
                self.__handleAddTransaction()
            elif op == "2":
                self.__handleDeleteTransaction()
            elif op == "3":
                self.__handleUpdateTransaction()
            elif op == "a":
                self.__handleShowList(self.__transactionService.getAll())
            elif op == "b":
                break
            else:
                print("Invalid option!")

    @staticmethod
    def __showMenuOthers():
        print(" ")
        print("---Others---")
        print("1.Search by")
        print("2.Show transactions with sum between")
        print("3.Show cars sorted by workmanship sum")
        print("4.Show cards sorted by discounts")
        print("5.Delete transactions from interval")
        print("6.Update guarantee")
        print("b.Back")
        print(" ")

    def __menuOthers(self):
        while True:
            self.__showMenuOthers()
            op = input("Option: ")
            if op == "1":
                self.__searchByMenu()
            elif op == "2":
                self.__handleFindTransactionBetweenSums()
            elif op == "3":
                self.__handleSortByWorkmanship()
            elif op == "4":
                self.__handleSortByDiscounts()
            elif op == "5":
                self.__handleDeleteTransactionsFromInterval()
            elif op == "6":
                self.__handleUpdateGuarantee()
            elif op == "b":
                break
            else:
                print("Invalid option!")

    @staticmethod
    def __showSearchByMenu():
        print(" ")
        print("---Search by---")
        print("1.Search cars by model")
        print("2.Search cars by acquisition year")
        print("3.Search cars by km number")
        print("4.Search clients by first name")
        print("5.Search clients by last name")
        print("6.Search clients by CNP")
        print("7.Search clients by birth date")
        print("8.Search clients by registration date")
        print("b.Back")
        print(" ")

    def __searchByMenu(self):
        while True:
            self.__showSearchByMenu()
            op = input("Option: ")
            if op == "1":
                model = input("Model: ")
                self.__handleShowList(self.__carService.searchByModel(model))
            elif op == "2":
                year = int(input("Year: "))
                self.__handleShowList(self.__carService.searchByYear(year))
            elif op == "3":
                km = float(input("Km number: "))
                self.__handleShowList(self.__carService.searchByKm(km))
            elif op == "4":
                name = input("First name: ")
                self.__handleShowList(self.__cardService.searchByFirstName(name))
            elif op == "5":
                name = input("Last name: ")
                self.__handleShowList(self.__cardService.searchByLastName(name))
            elif op == "6":
                CNP = int(input("CNP: "))
                self.__handleShowList(self.__cardService.searchByCNP(CNP))
            elif op == "7":
                date = input("Birth date: ")
                self.__handleShowList(self.__cardService.searchByBirthDate(date))
            elif op == "8":
                date = input("Registration date: ")
                self.__handleShowList(self.__cardService.searchByRegistrationDate(date))
            elif op == "b":
                break
            else:
                print("Invalid option!")

    def __handleAddCar(self):
        try:
            id = int(input("ID: "))
            model = input("Model: ")
            year = int(input("Acquisition Year: "))
            km = float(input("Number of kilometers: "))
            guarantee = input("In guarantee(True/False): ")
            if guarantee == "False":
                guarantee = False
            else:
                guarantee = True
            self.__carService.addCar(id, model, year, km, guarantee)
            print("The car was added successfully!")
        except CarValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleAddCard(self):
        try:
            id = int(input("ID: "))
            lastN = input("Last Name: ")
            firstN = input("First Name: ")
            CNP = int(input("CNP: "))
            bDate = input("Birth date(dd.mm.yyyy): ")
            rDate = input("Registration date(dd.mm.yyyy): ")
            self.__cardService.addCard(id, lastN, firstN, CNP, bDate, rDate)
            print("The card was added successfully!")
        except CardValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleAddTransaction(self):
        try:
            id = int(input("ID: "))
            carId = int(input("Car ID: "))
            cardId = int(input("Card ID: "))
            pieces = float(input("The price for pieces: "))
            workmanship = float(input("The price for workmanship: "))
            dateAndHour = input("The date and hour(dd.mm.yyyy hh:mm): ")
            self.__transactionService.addTransaction(id, carId, cardId, pieces, workmanship, dateAndHour)
            print("The transaction was added successfully!")
            for t in self.__transactionService.getTransactions():
                if t.entityId == id:
                    if t.discountPieces != 0:
                        print("Because the car is still in guarantee, the pieces are free!")
                        print("New price: " + str(t.pieces))
                    if t.discountWorkmanship != 0:
                        print("Because the client has a card, a discount of 10% is applied!")
                        print("New price: " + str(t.workmanship))
        except TransactionValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleDeleteCar(self):
        try:
            id = int(input("ID: "))
            self.__carService.deleteCar(id)
            print("The car was deleted successfully!")
        except ValueError:
            print("The id must be integer!")
        except Exception as e:
            print(e)

    def __handleDeleteCard(self):
        try:
            id = int(input("ID: "))
            self.__cardService.deleteCard(id)
            print("The card was deleted successfully!")
        except ValueError:
            print("The id must be integer!")
        except Exception as e:
            print(e)

    def __handleDeleteTransaction(self):
        try:
            id = int(input("ID: "))
            self.__transactionService.deleteTransaction(id)
            print("The transaction was deleted successfully!")
        except ValueError:
            print("The id must be integer!")
        except Exception as e:
            print(e)

    def __handleUpdateCar(self):
        try:
            id = int(input("ID: "))
            model = input("Model: ")
            year = int(input("Acquisition Year: "))
            km = float(input("Number of kilometers: "))
            guarantee = input("In guarantee(True/False): ")
            if guarantee == "False":
                guarantee = False
            else:
                guarantee = True
            self.__carService.updateCar(id, model, year, km, guarantee)
            print("The car was updated successfully!")
        except CarValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleUpdateCard(self):
        try:
            id = int(input("ID: "))
            lastN = input("Last Name: ")
            firstN = input("First Name: ")
            CNP = int(input("CNP: "))
            bDate = input("Birth date(dd.mm.yyyy): ")
            rDate = input("Registration date(dd.mm.yyyy): ")
            self.__cardService.updateCard(id, lastN, firstN, CNP, bDate, rDate)
            print("The card was updated successfully!")
        except CardValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleUpdateTransaction(self):
        try:
            id = int(input("ID: "))
            carId = int(input("Car ID: "))
            cardId = int(input("Card ID: "))
            pieces = float(input("The price for pieces: "))
            workmanship = float(input("The price for workmanship: "))
            dateAndHour = input("The date and hour(dd.mm.yyyy hh:mm): ")
            self.__transactionService.updateTransaction(id, carId, cardId, pieces, workmanship, dateAndHour)
            print("The transaction was updated successfully!")
        except TransactionValidationError as e:
            print("Errors:")
            for error in e.args[0]:
                print(error)
        except ValueError:
            print("Wrong input data")
        except Exception as e:
            print(e)

    def __handleDeleteTransactionsFromInterval(self):
        try:
            day1 = input("The beginning date(dd.mm.yyyy): ")
            day2 = input("The ending date(dd.mm.yyyy): ")
            self.__transactionService.deleteTransactionsFromDays(day1, day2)
        except Exception as e:
            print(e)

    @staticmethod
    def __handleShowList(objects):
        for object in objects:
            if object is not None:
                print(object)

    def __handleAddRandomCar(self):
        try:
            n = int(input("n = "))
            self.__carService.randomCars(n)
        except ValueError:
            print("Wrong input data")

    def __handleSortByWorkmanship(self):
        list = self.__transactionService.sortCarsByWorkmanship()
        self.__handleShowList(list)

    def __handleFindTransactionBetweenSums(self):
        try:
            sum1 = float(input("First sum: "))
            sum2 = float(input("Second sum: "))
            list = self.__transactionService.findTransactionsBetweenSums(sum1, sum2)
            self.__handleShowList(list)
        except ValueError:
            print("Wrong input data")

    def __handleUpdateGuarantee(self):
        self.__carService.updateGuarantee()

    def __handleSortByDiscounts(self):
        list = self.__transactionService.sortCardsByDiscounts()
        self.__handleShowList(list)

    @staticmethod
    def __handleShowPermutations(objects):
        i = 0
        for object in objects:
                i = i + 1
                print("Permutation " + str(i))
                for obj in object:
                    print(obj)
