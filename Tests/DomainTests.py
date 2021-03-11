from math import fabs

from Domain.Car import Car
from Domain.Card import Card
from Domain.Transaction import Transaction

EPSILON = 0.001


def test_car():

    c1 = Car(1, "Logan", 2010, 2345.7, True)
    assert c1.entityId == 1
    assert c1.model == "Logan"
    assert c1.acquisitionYear == 2010
    assert fabs(c1.kmNr - 2345.7) < EPSILON
    assert c1.inGuarantee is True


test_car()


def test_card():

    c1 = Card(1, "Pop", "Ion", 1960412123456, "12.04.1996", "21.10.2018")
    assert c1.entityId == 1
    assert c1.lastName == "Pop"
    assert c1.firstName == "Ion"
    assert c1.CNP == 1960412123456
    assert c1.birthDate == "12.04.1996"
    assert c1.registrationDate == "21.10.2018"


test_card()


def test_transaction():

    t1 = Transaction(1, 1, 1, 120.0, 40.0, "21.10.2018 14:34")
    assert t1.entityId == 1
    assert t1.carId == 1
    assert t1.cardId == 1
    assert fabs(t1.pieces - 120.0) < EPSILON
    assert fabs(t1.workmanship - 40.0) < EPSILON
    assert t1.dateAndHour == "21.10.2018 14:34"


test_transaction()
