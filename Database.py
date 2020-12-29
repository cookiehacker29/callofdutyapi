import json
import mysql.connector
import datetime
import time
import sys
import os

from mysql.connector.connection import MySQLConnection

class Database:
    def __init__(self) -> None:
        self.data : json                = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/config.json","r").read())["database"]
        self.mysql : MySQLConnection    = None
        

    def connect(self) -> None:
        try:
            self.mysql = mysql.connector.connect(
                host = self.data["host"],
                user = self.data["user"],
                passwd = self.data["password"],
                database = self.data["databasename"],
                port = self.data["port"]
            )   
        except:
            print("\033[1;31m[ERR]\033[0m Error with database connection, check your credential") 
            sys.exit("Error database !")
    
    def insertRatio(self, value : float) -> str:
        cursor = self.mysql.cursor()
        sql = "INSERT INTO RATIO (date,value) VALUES (%s,%s)"
        val = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),value)
        cursor.execute(sql,val)
        self.mysql.commit()
        return "["+val[0]+"] "+str(val[1])
