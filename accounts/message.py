from uuid import uuid4, UUID
from datetime import datetime

class Message:
    def __init__(self, content, fromuserid, touserid):
        """
        content - > Content of MEssage
        fromuserid -> user id of sender
        touserid -> User ID of Receiver
        timestamp -> Timestamp of creation
        """
        self.__content = content
        self.__from_user_id = UUID(fromuserid)
        self.__to_user_id = UUID(touserid)
        self.__timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def from_user_id(self):
        return self.__from_user_id
    @property
    def to_user_id(self):
        return self.__to_user_id
    @property
    def timestamp(self):
        return self.__timestamp
