from accounts.account import Account


class Admin(Account):
    def __init__(self, email: str,  username: str, name: str, password: str, uuid: str, accounttype: str = "admin"):
        super().__init__(username, password, uuid, accounttype)
        self.__email = email
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

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
