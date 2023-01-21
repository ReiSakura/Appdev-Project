# Made by ChangDe
# Filter for feedback

class Filter:
    def __init__(self, filter):
        self.__filter = filter

    def get_filter(self):
        return self.__filter

    def set_filter(self, filter):
        self.__filter = filter
