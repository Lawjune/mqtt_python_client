import sys
import os
sys.path.append((os.path.dirname(os.path.dirname(__file__))))

import time
from mqtt_client import MqttClient

host = "mqtt.eclipseprojects.io"
port = 1883
keepalive = 60

topic_a_to_b = "test/client_a_to_b"
topic_b_to_a = "test/client_b_to_a"

def main():
    client_a = MqttClient(host=host, port=port, keepalive=keepalive, client_id="test_client_a")
    client_b = MqttClient(host=host, port=port, keepalive=keepalive, client_id="test_client_b")
    client_a.add_topic(topic=topic_b_to_a)
    client_b.add_topic(topic=topic_a_to_b)

    client_a.start()
    client_b.start()

    time.sleep(4)

    client_a.publish(topic=topic_a_to_b, payload="Hello client b :)")
    client_b.publish(topic=topic_b_to_a, payload="Hi client a, how are you?")

    time.sleep(1)

    client_a.stop()
    client_b.stop()


if __name__ == "__main__":
    main()

