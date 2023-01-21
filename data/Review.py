# Made by Qinwen
# Objects for review
import uuid

class Review:

    def __init__(self, first_name, last_name, gender, rating, remarks):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__rating = rating
        self.__remarks = remarks
        self.__userID = uuid.uuid4()

# Getters
    def get_userID(self):
        return self.__userID
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_gender(self):
        return self.__gender
    def get_rating(self):
        return self.__rating
    def get_remarks(self):
        return self.__remarks
    def get_uuid(self):
        return self.__uuid

# Setters
    def set_userID(self, userID):
        self.__userID = userID
    def set_firstName(self,first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_gender(self, gender):
        self.__gender = gender
    def set_rating(self, rating):
        self.__rating = rating
    def set_remarks(self, remarks):
        self.__remarks = remarks

