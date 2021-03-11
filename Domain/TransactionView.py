class TransactionView:

    def __init__(self, transaction, car, card):
        self.transaction = transaction
        self.car = car
        self.card = card

    def __str__(self):
        return "{}. car: {} -- card: {}".format(self.transaction, self.car, self.card)
