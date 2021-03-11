from math import fabs

from Domain.Car import Car
from Domain.Card import Card
from Domain.Transaction import Transaction
from Repository.GenericFileRepository import GenericFileRepository

EPSILON = 0.001


def test_repository_car():
    r = GenericFileRepository("testCars.pkl")
    r.clear()
    c = Car(1, "Logan", 2010, 2345.7, True)
    r.create(c)
    assert len(r.read()) == 1
    c2 = Car(1, "Logan", 2011, 2345.7, True)
    r.update(c2)
    assert r.read()[0].acquisitionYear == 2011
    r.delete(c2.entityId)
    assert len(r.read()) == 0


test_repository_car()


def test_repository_card():
    r = GenericFileRepository("testCards.pkl")
    r.clear()
    c = Card(1, "Pop", "Ion", 1960412123456, "12.04.1996", "21.10.2018")
    r.create(c)
    assert len(r.read()) == 1
    c2 = Card(1, "Pop", "Ionica", 1960412123456, "12.04.1996", "21.10.2018")
    r.update(c2)
    assert r.read()[0].firstName == "Ionica"
    r.delete(c2.entityId)
    assert len(r.read()) == 0


test_repository_card()


def test_repository_transaction():
    r = GenericFileRepository("testTransactions.pkl")
    r.clear()
    t = Transaction(1, 1, 1, 120.0, 40.0, "21.10.2018 14:34")
    r.create(t)
    assert len(r.read()) == 1
    t2 = Transaction(1, 1, 1, 120.0, 50.0, "21.10.2018 14:34")
    r.update(t2)
    assert fabs(r.read()[0].workmanship - 50.0) < EPSILON
    r.delete(t2.entityId)
    assert len(r.read()) == 0


test_repository_transaction()
