import mysql.connector


class Model:
    def __init__(self, connection: mysql.connector.MySQLConnection, name: str):
        self.name = name
        self.conn = connection
        self.struct = []

    def _parse_result(self, data, struct=None):
        if type(data) == list:
            converted = []
            for i in data:
                d = self._parse_result(i)
                converted.append(d)
            return converted
        else:
            d = {}
            i = 0
            struct = (
                struct if struct else self.struct
            )  # Use the default if not provided
            for k in struct:
                d[k] = data[i]
                i += 1
            return d

    def _check_data(self, data) -> tuple:
        col_names = []
        values = []
        for i in data.keys():
            if i not in self.struct:
                raise Exception("Incorrect data structure")
            col_names.append(i)
            if type(data[i]) == int:
                values.append(data[i])
            else:
                values.append(f"'{data[i]}'")
        return col_names, values
