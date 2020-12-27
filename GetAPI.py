import requests
from Database import Database

from requests import *
import sys
import random
import json
import urllib

"""
=================
GetAPI class
=================

Class allowing to get the data of API of call of duty

"""
class GetAPI:
    """
        Constructor
    """
    def __init__(self) -> None:
        self.device_id : str    = str(hex(random.getrandbits(128)).lstrip("0x"))
        self.url_login : str    = "https://profile.callofduty.com/cod/mapp/login"
        self.url_device : str   = "https://profile.callofduty.com/cod/mapp/registerDevice"
        self.apibase : str      = "https://my.callofduty.com/api/papi-client/crm/cod/v2/"
        self.config : json      = json.loads(open("config.json","r").read())
        self.mysql : Database   = Database()
        

    """
    Fonction allowing to register any devices to get the access token
    """
    def registerDevice(self):
        mydata_device = {
            "deviceId" : self.device_id
        }

        device = post(self.url_device,json=mydata_device)

        return device
    
    """
    Login fonction, to get the access to the API and get the identities
    """
    def login(self) -> Response:

        device = self.registerDevice()

        if device.status_code == 200 :
            print("\033[1;32m[OK]\033[0m Device created....")

            mydata_login = {
                "email" : self.config["credential"]["username"],
                "password" : self.config["credential"]["password"]
            }

            access_token = json.loads(device.text)["data"]["authHeader"]

            headers_login = {
                "Authorization": f"Bearer "+access_token,
                "x_cod_device_id": self.device_id
            }

            login = post(url=self.url_login, json=mydata_login, headers=headers_login)

            return login

        else: sys.exit("Device error : "+device.status_code)

    """
    Fonction to access to the identities
    """
    def accessToIdentities(self) -> Response :
        login = self.login()
        if login.status_code == 200: 
            if json.loads(login.text)["success"]:
                print("\033[1;32m[OK]\033[0m Login success....")

                ident = post(url=self.apibase+"identities/", cookies=login.cookies)

                return (ident,login)
            else :
                print("\033[1;31m[ERR]\033[0m Login not valid, check your credential") 
                sys.exit(-1)
        else : sys.exit("Login error : " + login.status_code)

    """
    Fonction to access to the stats of user
    """
    def accessToStats(self) -> Response:
        access = self.accessToIdentities()
        ident = access[0]
        login = access[1]

        if ident.status_code == 200: 
            ident_data = json.loads(ident.text)
            if ident_data["status"] == "success":
                print("\033[1;32m[OK]\033[0m get Identities success....")

                data = ident_data["data"]["titleIdentities"][0]

                api_data = post(
                    url=
                        self.apibase+
                        "title/"
                        + data["title"] +
                        "/platform/"
                        + data["platform"] +
                        "/gamer/"
                        + urllib.parse.quote(data["username"]) +
                        "/matches/"
                        + data["activityType"] + 
                        "/start/0/end/0/details", cookies=login.cookies)

                return api_data
            else :
                print("\033[1;31m[ERR]\033[0m Login not valid, check your credential") 
                sys.exit(-1)
        else : sys.exit("Login error : " + login.status_code)

    """
    Fonction to get any data and save it on the database
    """
    def run(self) -> str:
        self.mysql.connect()
        api_data = self.accessToStats()
        
        if api_data.status_code == 200:
            print("\033[1;32m[OK]\033[0m API connexion success....")
            data_json = json.loads(api_data.text)
            
            self.mysql.insertRatio(data_json["data"]["summary"]["all"]["kdRatio"])
            return str(data_json["data"]["summary"]["all"]["kdRatio"])

