import paho.mqtt.client as mqtt
from backend import MyDB
from mqtt import EdgeCom

class Sensor:
    name: str
    location: str
    type: str
    period: int
    edge_client = None
    backend: MyDB

    def __init__(self, name: str, location: str, type: str, client: EdgeCom, backend: MyDB):
        self.name = name
        self.location = location
        self.type = type
        self.edge_client = client
        self.backend = backend

    def __str__(self):
        return "[" + self.name + "@" + self.location + "/" + self.type + "]"
    
    def on_data_recv(self, data):
        print("{} Data received: {}.".format(str(self), str(data)))
        self.backend.add_measurement(self.location, self.type, int(data))

    def start(self):
        self.edge_client.add_sensor(self)
    
    def stop(self):
        self.edge_client.remove_sensor(self)