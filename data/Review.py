# created by Qinwen
#Objects for review

# Note to Jens: uuid no need bah i never put idk

class Review():
    def __init__(self, first_name, last_name, gender, rating, remarks):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__rating = rating
        self.__remarks = remarks

    # Getters
    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_remarks(self):
        return self.__remarks

    # Setters

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_remarks(self, remarks):
        self.__remarks = remarks