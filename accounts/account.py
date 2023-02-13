import shelve
from time import time
from hashlib import sha256


class Account:
    """
    username: Username -> String
    password: Account Password - > String  Stored in SHA265
    uuid: UUID -> Array of Strings["For Multi-Device Login"]

    messages : {} -> UUID(To User ID) : Array of Messages
    """

    def __init__(self, username: str, password: str, uuid: str, accounttype: str):
        self.__username = username
        self.__password = sha256(bytes(password, 'UTF-8')).hexdigest()
        self.__uuid = uuid
        self.__last_entered = time()
        self.__account_type = accounttype
        self.__messages = {}

    @property
    def username(self):
        """
        Return Username
        """
        return self.__username

    @username.setter
    def username(self, username):
        """
        Sets Username
        """
        self.__username = username

    @property
    def password(self):
        """
        Return Password
        """
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def last_entered(self):
        """
        Return time last_entered
        """
        return self.__last_entered

    @last_entered.setter
    def last_entered(self, le):
        """
        Sets time last_entered
        """
        self.__last_entered = le

    @property
    def uuid(self):
        """
        Return uuid
        """
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        """
        Sets uuid
        """
        self.__uuid = uuid

    @property
    def accounttype(self):
        """
        Return account's type
        """
        return self.__account_type

    @accounttype.setter
    def accounttype(self, at):
        """
        Sets account's type
        """
        self.__account_type = at

    @property
    def messages(self):
        """
        Return's Dictionary of Chats with Users

        """
        return self.__messages

    @messages.setter
    def messages(self, messages):
        self.__messages = messages
