# Made by amanda
# Objects for inventory
import uuid


class Product():
    def __init__(self, name="", category="", quantity=0, price=0):
        self.__name = name
        self.__category = category
        self.__quantity = quantity
        self.__price = price
        self.__uuid = uuid.uuid4()

    # Setters
    def getName(self):
        return self.__name

    def getCategory(self):
        return self.__category

    def getQuantity(self):
        return self.__quantity

    def getPrice(self):
        return self.__price

    def getuuid(self):
        return self.__uuid

    # Getters
    def setName(self, name):
        self.__name = name

    def setCategory(self, category):
        self.__category = category

    def setQuantity(self, quantity):
        self.__quantity = quantity

    def setPrice(self, price):
        self.__price = price
