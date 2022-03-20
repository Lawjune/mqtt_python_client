import paho.mqtt.client as mqtt
import logging

from common.safe_thread import SafeThread

mqtt_connection_return_code = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorised"
}

class MqttClient(SafeThread):
    def __init__(self, host, port, keepalive, client_id="", logging_level=logging.DEBUG):
        super(MqttClient, self).__init__(logging_level)
        self.__host = host
        self.__port = port
        self.__keepalive = keepalive
        self.__client_id = client_id
        self.__client = mqtt.Client(client_id=client_id)
        self.__on_connect_callback = None
        self.__on_message_callback = None
        self.__on_publish_callback = None
        self.__on_subscribe_callback = None
        self.__to_subscribe_topics = list()

    def run(self):
        self.logger.debug("Start running.")
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_subscribe = self.__on_subscribe
        self.logger.debug(f"{self.__client_id} trying to connect to {self.__host}:{self.__port}")
        self.__client.connect(host=self.__host, port=self.__port, keepalive=self.__keepalive)
        self.__client.loop_start()

    def stop(self):
        self.__client.loop_stop()
        super(MqttClient, self).stop()

    def publish(self, topic, payload=None, qos=0, retain=False):
        self.logger.debug(f"[{self.__client_id}] Publishing '{payload}' to '{topic}' with qos={qos}")
        self.__client.publish(topic, payload, qos, retain)

    def add_topic(self, topic):
        self.__to_subscribe_topics.append(topic)

    
    # Subcribe must be executed under on_connect
    def __subscribe(self, topic, qos=0):
        self.logger.debug(f"[{self.__client_id}] Subscribing topic: '{topic}' with qos={qos}")
        self.__client.subscribe(topic, qos)

    def set_on_connect_callback(self, callback):
        self.__on_connect_callback = callback

    def set_on_message_callback(self, callback):
        self.__on_message_callback = callback

    def set_on_publish_callback(self, callback):
        self.__on_publish_callback = callback

    def set_on_subscribe_callback(self, callback):
        self.__on_subscribe_callback = callback

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        self.__core_on_subscribe_callback(client, userdata, mid, granted_qos)
        if self.__on_subscribe_callback:
            self.__on_subscribe_callback(client, userdata, mid, granted_qos)

    def __on_publish(self, client, userdata, mid):
        self.__core_on_publish_callback(client, userdata, mid)
        if self.__on_publish_callback:
            self.__on_publish_callback(client, userdata, mid)

    def __on_connect(self, client, userdata, flags, rc):
        self.__core_on_connect_callback(client, userdata, flags, rc)
        if self.__on_connect_callback:
            self.__on_connect_callback(client, userdata, flags, rc)

    def __on_message(self, client, userdata, msg):
        self.__core_on_message_callback(client, userdata, msg)
        if self.__on_message_callback:
            self.__on_message_callback(client, userdata, msg)

    def __core_on_subscribe_callback(self, client, userdata, mid, granted_qos):
        self.logger.debug(f"[{self.__client_id}] Subscribed result {mid}")

    def __core_on_publish_callback(self, client, userdata, mid):
        self.logger.debug(f"[{self.__client_id}] Publishded result {mid}")

    def __core_on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug(f"{self.__client_id}: Connected {self.__host}:{self.__port} with result code "
                          f"{str(rc)} - {mqtt_connection_return_code[rc]}")

        if len(self.__to_subscribe_topics) > 0:
            for topic in self.__to_subscribe_topics:
                self.__subscribe(topic)

    def __core_on_message_callback(self, client, userdata, msg):
        self.logger.debug(f"[{self.__client_id}] received '{msg.topic}' {str(msg.payload)}")


if __name__ == "__main__":
    import time

    host = "mqtt.eclipseprojects.io"
    port = 1883
    keepalive = 60

    mc = MqttClient(host=host, port=port, keepalive=keepalive)
    mc.start()
    time.sleep(3)
    mc.stop()
