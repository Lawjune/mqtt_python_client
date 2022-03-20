import sys
import os
sys.path.append((os.path.dirname(os.path.dirname(__file__))))

import time
from mqtt_client import MqttClient

host = "127.0.0.1"
port = 1883
keepalive = 60


def main():
    client_a = MqttClient(host=host, port=port, keepalive=keepalive, client_id="test_client")

    client_a.start()

    time.sleep(4)
    client_a.stop()



if __name__ == "__main__":
    main()

