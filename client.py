import paho.mqtt.client as mqtt
import json

def create_client(sub_topic, topic, value, host, port):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " +str(rc))
        client.subscribe(sub_topic)
    
    def on_message(client, userdata, msg):
        try:
            topic = msg.topic
            x = json.loads(msg.payload.decode('utf-8'))
            print(f"Pesan masuk : {x}")
            value = x
            changed = True
        except Exception as e:
            print("ERROR!", e)

    client = mqtt.CLient()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 60)

    return client