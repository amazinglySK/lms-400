import mysql.connector

from .model import Model
from ..exceptions import MemberNotFoundError


class Member(Model):
    def __init__(self, connection: mysql.connector.MySQLConnection):
        super().__init__(connection, "members")
        self.cursor = self.conn.cursor()
        self.struct = [
            "member_code",
            "member_address",
            "member_phone",
            "maximum_limit",
            "no_issued",
        ]

        try:
            self.cursor.execute(f"select * from {self.name}")
        except:
            self.cursor.execute(
                f"create table {self.name}(member_code int, member_address varchar(30), member_phone varchar(12), maximum_limit int, no_issued int)"
            )

    def new(self, details: dict):
        col, values = self._check_data(details)
        col_str = ", ".join(col)
        val_str = ", ".join(values)
        self.cursor.execute(f"insert into {self.name} ({col_str}) values({val_str})")
        self.conn.commit()
        return

    def get_all_members(self):
        self.cursor.execute(f"select * from {self.name}")
        results = self.cursor.fetchall()
        results = self._parse_result(results)
        return results

    def get_member(self, member_code):
        self.cursor.execute(
            f"select * from {self.name} where member_code == {member_code}"
        )
        results = self.cursor.fetchall()
        if self.cursor.rowcount == 0:
            raise MemberNotFoundError
        results = self._parse_result(results)
        return results

    def update_details(self, details: dict, member_code: int):
        col, values = self._check_data(details)
        cmd_str = ""
        for c, v in zip(col, values):
            cmd_str += f"{c} = {v},"
        cmd = cmd_str[:-1]
        cmd = f"update {self.name} set {cmd} where member_code = {member_code}"
        self.cursor.execute(cmd)
        self.conn.commit()
        return
