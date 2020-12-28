from GetAPI import GetAPI

import threading
import time

stop_threads : bool = False

"""
Fonction allowing to refresh data all the 60 seconds on a thread
"""
def getapi_thread() -> None:
    myapi : GetAPI = GetAPI()
    myapi.login()
    while(1):
        print("\033[1;34m[INFO]\033[0m Update DATA") 
        myapi.run()
        time.sleep(60)
        global stop_threads
        if stop_threads:
            break

"""
Code allowing to start thread and reset cookies one time by days
"""
while(1):
    print("\033[1;34m[INFO]\033[0m Start application !") 
    x : threading.Thread = threading.Thread(target=getapi_thread,args=())
    x.start()
    time.sleep(86400)
    stop_threads : bool = True
    x.join()
    print("\033[1;34m[INFO]\033[0m Reset of cookies") 
    stop_threads : bool = False
    


