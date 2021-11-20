#! /usr/bin/python3.9
from sensors import Sensor
from mqtt import EdgeCom
from backend import MyDB
import signal

class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    backend = MyDB("https://homebase-2a426-default-rtdb.europe-west1.firebasedatabase.app/")
    client = EdgeCom("awax.local")
    tempSensor = Sensor("temp", "livingRoom", "temp", client, backend).start()    
    humidSensor = Sensor("humid", "livingRoom", "humid", client, backend).start()


    while True:
        try:
            pass
        except ProgramKilled:
            client.stop()
            #TODO send a mail notifying that the server has shutdown
            exit(1)
