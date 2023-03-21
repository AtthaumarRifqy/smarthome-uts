# Sumber Code : https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

# Import Library
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

# Deaktivasi Debug Output dan aktivasi Garbage Collector
# karena ini merupakan stable release MicroPython, Debug Output seharusnya sudah
# terdeaktivasi secara otomatis, namun kode berikut tetap disimpan untuk memastikan
esp.osdebug(None)
import gc
gc.collect()

# Network Credentials
ssid = 'Just connect to the wifi...'
password = 'nopasswordobviously'
mqtt_server = '192.168.118.173'

# Get board's unique ID and set the topic it will publish to
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'smarthome/#'
topic_pub_ac = b'smarthome/ac/status'
topic_pub_light = b'smarthome/light/status'

# Define constants
acOn = False
lightOn = False

device = ''
msg = ''
change = False

# Create network connection
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
