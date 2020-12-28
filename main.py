from GetAPI import GetAPI

import threading
import time

stop_threads = False

def getapi_thread():
    myapi = GetAPI()
    myapi.login()
    while(1):
        print("\033[1;34m[INFO]\033[0m Update DATA") 
        myapi.run()
        time.sleep(60)
        global stop_threads
        if stop_threads:
            break

while(1):
    print("\033[1;34m[INFO]\033[0m Start application !") 
    x = threading.Thread(target=getapi_thread,args=())
    x.start()
    time.sleep(86400)
    stop_threads = True
    x.join()
    print("\033[1;34m[INFO]\033[0m Reset of cookies") 
    stop_threads = False
    


