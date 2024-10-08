from django.apps import AppConfig
from threading import Thread
import paho.mqtt.client as paho
from paho import mqtt

broker = '7e68437c2d4d4cc185d83eb266d03aaa.s1.eu.hivemq.cloud'
port = 8883
topic = "Sensor_Data"
client_id = 'server_iot'

class MqttClient(Thread):
    def __init__(self, broker, port, timeout, topics):
        super(MqttClient, self).__init__()
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION1,client_id="server_iot", userdata=None, protocol=paho.MQTTv5)
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.topics = topics
        self.total_messages = 0
    #  run method override from Thread class
    def run(self):
        self.connect_to_broker()
    def connect_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, self.timeout)
        # self.client.loop_forever()
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        self.total_messages = self.total_messages + 1
        print(str(msg.payload) + "Total: {}".format(self.total_messages))
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        #  Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
        print("success")
        for topic in self.topics:
            client.subscribe(topic)


class DatamanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'datamanagement'

    def ready(self):
        from . import signals
        # MqttClient(broker, port, 60, topic).start()
