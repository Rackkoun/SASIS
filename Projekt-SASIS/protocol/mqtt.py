"""
    Created on 05.08.2019 at 22:12
    @author: Ruphus
    source: steves-internet-guide.com
"""
import time
import paho.mqtt.client as mqtt
import datetime as dt

class SASISWarmingMQTT:

    def __init__(self):
        self.instance = mqtt.Client(client_id="SASIS-Warning-V01", clean_session=False)

        self.instance.on_message = self.on_message
        self.instance.on_log = self.on_log
        self.instance.on_publish = self.on_publish
        self.instance.on_disconnect = self.on_disconnect

    def on_connect_to_broker(self, broker, port, alive):
        self.instance.connect(host=broker, port=port, keepalive=alive)

    def on_publishing(self, topic, msg, qos):
        self.instance.publish(topic=topic, payload=msg, qos=qos)
        time.sleep(1)
        print("Value published: ", msg)
        time.sleep(1)
        self.instance.loop_stop()
        self.instance.disconnect()
        today = dt.datetime.now().strftime("%Y-%b-%d %H:%M")
        print("Disconnected on ", today)

    def on_message(self, client, userdata, msg):
        print("Message received: ", str(msg.payload.decode('utf-8')))
        print("Topic: ", msg.topic)
        print("QoS: ", msg.qos)
        print("Retained Msg: ", msg.retain)

    def on_log(self, client, userdata, level, buf):
        print("Logger: ", buf)

    def on_publish(self, client, userdata, result):
        print("Data Sent with result: ", result)

    def on_disconnect(self, client, userdata, rc):
        print(client, "disconnected successfully!")