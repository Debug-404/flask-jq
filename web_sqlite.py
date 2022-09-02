import sqlite3


class My_sqlite:
    def __init__(self, sqlName):
        self.sqlName = sqlName

    def __enter__(self):
        self.conn = sqlite3.connect(self.sqlName)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_avl, exc_tb):
        self.cursor.close()
        self.conn.close()

    def register(self, user: str, paw: str) -> bool:
        """
        注册信息(学号,密码) 成功返回Ture
        """
        sql = f"insert into web_db(No,pad) values('{user}','{paw}');"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def login(self, user: str) -> bool:
        """
        判断某个学号是否可以登录(web表)
        """
        sql = f"select count(*) from web_db where No='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def selPassword(self, user: str, paw: str) -> bool:
        """
        查询输入的密码与数据库的密码是否一致。相同返回Ture
        """
        sql = f"SELECT pad FROM web_db WHERE No='{user}'"
        if self.cursor.execute(sql).fetchall()[0][0] == paw:
            return True
        else:
            return False

    def getStudentInfo(self) -> list:
        """
        返回数据库里的学生信息
        """
        sql = "SELECT 学号,姓名,性别 FROM student_info"
        date = self.cursor.execute(sql).fetchall()
        return date

    def intoAdmin(self, user: str, paw: str) -> bool:
        """
        向数据库中写入学生的学号,密码。学号为主键。
        """
        sql = f"insert into web_db(No,pad) values('{user}','{paw}');"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def intoStudentInfo(self, user: str, name: str, sex: str) -> bool:
        """
        往数据库中写入学生信息
        """
        sql = f"INSERT INTO student_info (学号,姓名,性别) VALUES('{user}','{name}','{sex}')"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def stuinMysql(self, user: str) -> bool:
        """
        判断某个学号是否存在于数据库中(student_info表) 存在return Ture
        """
        sql = f"select count(*) from student_info where 学号='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def delStudent(self, user: str) -> bool:
        """
        删除学生信息
        """
        if self.stuinMysql(user):
            sql = f"DELETE FROM student_info WHERE 学号='{user}'"
            try:
                self.cursor.execute(sql)
            except:
                return False
            self.conn.commit()
            return True

    def upDataStudent(self, user: str, name: str, sex: str) -> None:
        """
        更新学生信息
        """
        sql = f"UPDATE student_info set 姓名='{name}',性别='{sex}' WHERE 学号='{user}'"
        self.cursor.execute(sql)
        self.conn.commit()

    def getOneStudent(self, user: str) -> list:
        """
        获取某个学生信息
        """
        sql = f"SELECT * FROM student_info WHERE 学号='{user}'"
        return self.cursor.execute(sql).fetchall()


# with My_sqlite("student.db") as name:name.getStudentInfo()

def register(database: My_sqlite, user: str, paw: str) -> bool:
    """
    注册信息(学号,密码) 成功返回Ture
    """
    with database:
        return database.register(user, paw)


def loGin(database: My_sqlite, user: str) -> bool:
    """
    判断某个学号是否可以登录(web表)
    """
    with database:
        return database.login(user)


def selPassword(database: My_sqlite, user: str, paw: str) -> bool:
    """
    查询输入的密码与数据库的密码是否一致。相同返回Ture
    """
    with database:
        return database.selPassword(user, paw)


def getStudentInfo(database: My_sqlite) -> tuple:
    """
    返回数据库里的学生信息
    """
    with database:
        return database.getStudentInfo()


def intoAdmin(database: My_sqlite, user: str, paw: str) -> bool:
    """
    向数据库中写入学生的学号,密码。学号为主键。
    """
    with database:
        return database.intoAdmin(user, paw)


def intoStudentInfo(database: My_sqlite, user: str, name: str, sex: str) -> bool:
    """
    往数据库中写入学生信息
    """
    with database:
        return database.intoStudentInfo(user, name, sex)


def stuinMysql(database: My_sqlite, user: str) -> bool:
    """
    判断某个学号是否存在于数据库中(student_info表) 存在return Ture
    """
    with database:
        return database.stuinMysql(user)


def delStudent(database: My_sqlite, user: str) -> bool:
    """
    删除学生信息
    """
    with database:
        return database.delStudent(user)


def upDataStudent(database: My_sqlite, user: str, name: str, sex: str) -> None:
    """
     更新学生信息
    """
    with database:
        database.upDataStudent(user, name, sex)


def getOneStudent(database: My_sqlite, user: str) -> list:
    """
    获取某个学生信息
    """
    with database:
        return database.getOneStudent(user)
