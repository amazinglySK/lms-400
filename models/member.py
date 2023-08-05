import mysql.connector

from .model import Model


class MemberNotFoundError(Exception):
    def __init__(self):
        super().__init__("Member not found")


class Member(Model):
    def __init__(self, connection: mysql.connector.MySQLConnection):
        super().__init__(connection, "members")
        self.cursor = self.conn.cursor()
        self.struct = [
            "member_code",
            "name",
            "address",
            "phone",
            "maximum_limit",
            "no_issued",
        ]

        try:
            self.cursor.execute(f"select * from {self.name}")
            r = self.cursor.fetchall()
        except:
            self.cursor.execute(
                f"create table {self.name}(member_code int primary key auto_increment, name varchar(20), address varchar(30), phone varchar(12), maximum_limit int default(3), no_issued int default(0))"
            )
            self.conn.commit()

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

    def search_member_by_name(self, member_name: str) -> bool | list[dict]:
        self.cursor.execute(
            f"select * from {self.name} where name like '%{member_name}%'"
        )
        results = self.cursor.fetchall()
        if self.cursor.rowcount == 0:
            return False
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
