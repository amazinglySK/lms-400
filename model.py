import mysql.connector


class Config:
    def __init__(self, pwd, db, host="localhost", user="root"):
        self.host = host
        self.pwd = pwd
        self.user = user
        self.db = db


class Model:
    def __init__(self, name: str, schema: dict, config: Config):
        self.name = name
        self.schema = schema
        self.config = config
        self.cursor = self._connect()

        # TODO : Do this only when table doesn't exist
        self._new_table()

    def _connect(self):
        c = self.config
        connection = mysql.connector.connect(
            host=c.host,
            user=c.user,
            password=c.pwd,
            db=c.db,
        )
        cursor = connection.cursor()
        return cursor

    def _format_create_command(self):
        create_str = f"create table {self.name} values({', '.join([' '.join((k, v)) for k,v in self.schema.items()])});"

        return create_str

    def _new_table(self):
        cmd = self._format_create_command()
        self.cursor.execute(cmd)
        self.cursor.commit()

    def new_entry(self, vals: dict):
        # insert into <table name> () vals();
        cmd = f"insert into {self.name} table ({', '.join(vals.keys())} values({', '.join(vals.values())});"
        self.execute(cmd)

    def _required_columns(self, cmd):
        cmd = cmd.replace(", ", ",")
        split = cmd.split(" ")
        split[1]
        if split[1] == "*":
            return dict.fromkeys(self.schema.keys())
        sp_split = split.split(",")
        req_dict = {}  # The dictionary that'll be returned
        for i in sp_split:
            if i.lower() in self.keys():
                req_dict.setdefault(i)

        return req_dict

    def execute(self, cmd: str, select=False):
        self.cursor.execute(cmd)
        self.cursor.commit()

        if select:
            result = self.cursor.fetchall()
            fields = []
            for r in result:
                field_set = self._required_columns(cmd)
                i = 0
                for k in field_set:
                    field_set[k] = r[i]
                    i += 1

                fields.append(field_set)
            return fields
