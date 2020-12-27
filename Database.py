import json
import mysql.connector
import datetime
import time

class Database:
    def __init__(self) -> None:
        data = json.loads(open("config.json","r").read())["database"]
        self.mysql = mysql.connector.connect(
            host = data["host"],
            user = data["user"],
            passwd = data["password"],
            database = data["databasename"],
            port = data["port"]
        )
    
    def insertRatio(self, value : float):
        cursor = self.mysql.cursor()
        sql = "INSERT INTO RATIO (date,value) VALUES (%s,%s)"
        val = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),value)
        cursor.execute(sql,val)
        self.mysql.commit()
