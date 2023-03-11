
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import CMySQLConnection
class MySQLConnection:
    def __init__(self):
        print("executed")
        self.config = {
        'user': 'root',
        'password': 'mubeen',
        'port':'3306',
        'host': '127.0.0.1',
        'database': 'fastapi',
        'raise_on_warnings': True
        }

        self.cnx = ""
        try:
            self.cnx = mysql.connector.connect(**self.config)
            # print(f"Connection object details = {self.cnx}")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        # else:
        #     return self.cnx
    def connection_object(self):
        return self.cnx