"""
Table Structure
1) Columns -> dictionary(Column Name : Column Data(Array))
2) Rows -> Array -> Dictionary/Object

The Table Data should be sorted from Earliest Date to Latest Date

Note: If you want to show Latest Date by default, just do sorted(self.rows, reverse=True)
"""


class Table:
    def __init__(self, *args):
        """
        1) Args -> Obtain all column names
        """
        self.__columns = {}
        self.__rows = []  # 2D Array when inserting rows
        for x in args:
            self.__columns[str(x)] = []

    def insertRow(self, row: dict) -> bool:
        """
        Inserts Row into table
        """
        if len(row.keys()) == len(self.__columns):
            self.__rows.append(row)
            for key, value in row.items():
                self.__columns[key].append(value)
            return True
        else:
            print(
                f"TableError: Unable To Insert Row Due to Unequal Number of Rows\nNeeded {len(row)}, {len(self.columns)} was given")
            return False

    def getColumn(self, column):
        """
        Returns All Data in a specified Column
        """
        col = []
        for x in self.__rows:
            col.append(x[column])
        return col

    @property
    def columns(self):
        """
        Returns Column Names
        """
        return self.__columns.keys()

    @property
    def rows(self):
        """
        Returns All Rows
        """
        return self.__rows

    def alphabetSort(self, column):
        """
        Returns New Table Sorted Alphabetically(Based on which Column is Selected)
        """
        return sorted(self.__rows)

    # Query must be equivalent
    def finditem_eq(self, query: str = "") -> [bool, []]:
        """
        Strict Equivalent Query Search(Based on Main Search)
        """
        selected = []
        for x in self.__rows:
            if (query in x.values()):
                selected.append(x)

        if len(selected) != 0:
            return [True, selected]
        else:
            return [False, selected]

    def finditem(self, query: str = "") -> [bool, []]:  # Main Search
        """
        Main Search algorithm
        """
        selected = []
        for x in self.__rows:
            for y in x.values():
                try:
                    if (query.lower() in str(y).lower()):
                        selected.append(x)
                        break
                except:
                    continue

        if len(selected) != 0:
            return [True, selected]
        else:
            return [False, selected]

    # Search in column
    def finditem_col_eq(self, column: str, query: str = "") -> [bool, []]:
        """
        Search Algorithm in Column
        Purpose is to prevent issues with conflicting usernames
        And to allow for others username to possibly be someone's password(can be removed)
        """
        selected = []
        c = self.getColumn(column)
        for x in c:
            if query == x:
                selected.append(x)
                break

        if len(selected) != 0:
            return [True, selected]
        else:
            return [False, selected]
