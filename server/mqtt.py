import paho.mqtt.client as mqtt

class EdgeCom:
    mqtt_client: mqtt
    topics = {}
    
    def __init__(self, addr):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(addr, 1883, 60)
        self.mqtt_client.loop_start()

    def add_sensor(self, sensor):
        topic = sensor.location + "/" + sensor.type
        self.topics[topic] = sensor
        self.mqtt_client.subscribe(topic)
    
    def remove_sensor(self, sensor):
        topic = sensor.location + "/" + sensor.type
        if self.topics.pop(topic, None) is not None:
            self.mqtt_client.unsubscribe(topic)
        
    def on_connect(self, client, userdata, flags, rc):
        print("mqtt client: connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic, callback in self.topics.items():
            client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        sensor = self.topics[msg.topic]
        #call the sensor callback
        sensor.on_data_recv(msg.payload)
    
    def send(self, topic, msg):
        self.mqtt_client.publish(topic, msg)

    def stop(self):
        print("Stopping the mqtt client thread.")
        self.mqtt_client.loop_stop()
        