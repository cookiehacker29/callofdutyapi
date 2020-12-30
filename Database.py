import json
import mysql.connector
import datetime
import time
import sys
import os

from mysql.connector.connection import MySQLConnection

"""
=================
Database class
=================

Class allowing to interact with the MySQL database for insert data from the call of duty API

Example of use : 

    mydb : Database = Database()
    mydb.connect()
    mydb.insertRatio(5.0)
"""
class Database:
    def __init__(self) -> None:
        self.data : json                = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/config.json","r").read())["database"]
        self.mysql : MySQLConnection    = None
        
    """
    Fonction allowing to connect on the database
    """
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
    
    """
    Fonction allowing to insert the ratio value on the databse
    """
    def insertRatio(self, value : float) -> str:
        cursor = self.mysql.cursor()
        sql = "INSERT INTO RATIO (date,value) VALUES (%s,%s)"
        val = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),value)
        cursor.execute(sql,val)
        self.mysql.commit()
        return "["+val[0]+"][RATIO] "+str(val[1])
