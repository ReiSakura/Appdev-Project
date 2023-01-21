import uuid

class Announcement:

    def __init__(self, title, content):
        self.__title = title
        self.__content = content
        self.__announcement_id = uuid.uuid4()

    # Getters and setters
    def get_announcement_id(self):
        return self.__announcement_id

    def set_announcement_id(self, announcement_id):
        self.__announcement_id = announcement_id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content
