import shelve
import os
"""
Serve for easier access to Database
Database Structure
Dictionary
Table Name : Table Class(From Table.py)

self.__db -> symbolic link with the database(Any changes to it would immediately affect the database)

"""


class Database():
    def __init__(self):
        self.__db = shelve.open(f"{os.getcwd()}/storage/database", "c")
        try:

            self.__tables = self.__db["tables"]
        except:
            self.__tables = {}

    def open(self):
        self.__db = shelve.open(f"{os.getcwd()}/storage/database", "c")

    @property
    def tables(self):
        return self.__tables

    @tables.setter
    def update_tables(self, tables):
        self.__tables = tables

    def commit(self):
        self.open()
        self.__db["tables"] = self.__tables
        self.__db.close()

    def close(self):
        self.__db["tables"] = self.__tables
        self.__db.close()
