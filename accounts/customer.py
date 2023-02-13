
from data.table import Table
from accounts.account import Account


class Customer(Account):
    def __init__(self, username: str, email: str,  name: str, address: str, password: str, uuid: str, accounttype: str = "customer"):
        super().__init__(username, password, uuid, accounttype)
        self.__address = address
        self.__email = email
        self.__name = name
        self.__invoices = Table("products")
        self.__cart = []

    @property
    def address(self):
        """
        Returns Customer Address
        """
        return self.__address

    @address.setter
    def address(self, address: str):
        """
        Sets Customer Address
        """
        self.__address = address

    @property
    def name(self):
        """
        Returns customer's name
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Sets Customer's Name

        """
        self.__name = name

    @property
    def email(self):
        """
        Returns customer's name
        """
        return self.__email

    @email.setter
    def email(self, email: str):
        """
        Sets Customer's Name

        """
        self.__email = email

    @property
    def cart(self):
        """
        Returns customer's cart
        """
        try:
            return self.__cart
        except:
            self.__cart = []
            return self.__cart

    @cart.setter
    def cart(self, cart: list):
        """
        Sets Customer's Name

        """
        self.__cart = cart
