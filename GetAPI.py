from requests import *
import sys
import random
import json

"""
=================
GetAPI class
=================

Class allowing to get the data of API of call of duty

"""
class GetAPI:
    def __init__(self) -> None:
        self.device_id      = str(hex(random.getrandbits(128)).lstrip("0x"))
        self.url_login      = "https://profile.callofduty.com/cod/mapp/login"
        self.url_device     = "https://profile.callofduty.com/cod/mapp/registerDevice"
        self.url_api        = "https://my.callofduty.com/api/papi-client/crm/cod/v2/title/mw/platform/battle/gamer/CookieHacker%232929/matches/mp/start/0/end/0/details"
        self.config         = json.loads(open("config.json","r").read())

    def registerDevice(self):
        mydata_device = {
            "deviceId" : self.device_id
        }

        device = post(self.url_device,json=mydata_device)

        return device
    
    def login(self):

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


    def accessToStats(self):
        login = self.login()

        if login.status_code == 200: 
            if json.loads(login.text)["success"]:
                print("\033[1;32m[OK]\033[0m Login success....")

                api_data = post(url=self.url_api, cookies=login.cookies)

                return api_data
            else :
                print("\033[1;31m[ERR]\033[0m Login not valid, check your credential") 
                sys.exit(-1)
        else : sys.exit("Login error : " + login.status_code)

    def run(self):
        api_data = self.accessToStats()

        if api_data.status_code == 200:
            print("\033[1;32m[OK]\033[0m API connexion success")
            data_json = json.loads(api_data.text)
            return str(data_json["data"]["summary"]["all"]["kdRatio"])

