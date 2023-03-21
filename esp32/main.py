# Sumber Code MQTT : https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/
# Pengetahuan TouchPad bersumber dari : https://www.upesy.com/blogs/tutorials/use-esp32-built-in-capacitive-touch-sensor-pins-with-micro-python
# Pengetahuan Timer bersumber dari : https://docs.micropython.org/en/latest/library/machine.Timer.html

from machine import Timer, Pin
from time import sleep

led = Pin(2, Pin.OUT)
timer = Timer(0)
timer_ac = Timer(1)
timer_light = Timer(2)
timer_all = Timer(3)

def switchLed(t):
    led.value(not led.value())

def startAc(t):
    global client, acOn, lightOn
    
    try:
        timer.deinit()
    except:
        pass
    finally:
        timer.init(mode=Timer.PERIODIC, freq=5, callback=switchLed)
        acOn = True
        lightOn = False

    client.publish('smarthome/ac/status', handleMessage(acOn))

def startLight(t):
    global client, lightOn
    
    try:
        timer.deinit()
    except:
        pass
    finally:
        timer.init(mode=Timer.PERIODIC, freq=20, callback=switchLed)
        lightOn = True
    
def startAll(t):
    try:
        timer.deinit()
    except:
        pass
    finally:
        led.value(1)

def offAll(t):
    try:
        timer.deinit()
    except:
        pass
    finally:
        led.value(0)
    
def handleAc(msg):
    global acOn, lightOn
    
    period_start = int(msg[1]) * 1000
    
    try:
        timer_ac.deinit()
    except:
        pass
    
    if msg[0] == 'on' and lightOn:
        timer_ac.init(mode=Timer.ONE_SHOT, period=period_start, callback=startAll)
    elif msg[0] == 'on' and not lightOn:
        timer_ac.init(mode=Timer.ONE_SHOT, period=period_start, callback=startAc)
    elif msg[0] == 'off' and lightOn:
        timer_ac.init(mode=Timer.ONE_SHOT, period=period_start, callback=startLight)
    elif msg[0] == 'off' and not lightOn:
        timer_ac.init(mode=Timer.ONE_SHOT, period=period_start, callback=offAll)
    else:
        print("Error! Invalid command")
    
    if msg[0] == 'on':
        acOn = True
    elif msg[0] == 'off':
        acOn = False
    
def handleLight(msg):
    global acOn, lightOn
    
    period_start = int(msg[1]) * 1000
    
    try:
        timer_light.deinit()
    except:
        pass
    
    if msg[0] == 'on' and acOn:
        timer_light.init(mode=Timer.ONE_SHOT, period=period_start, callback=startAll)
    elif msg[0] == 'on' and not acOn:
        timer_light.init(mode=Timer.ONE_SHOT, period=period_start, callback=startLight)
    elif msg[0] == 'off' and acOn:
        timer_light.init(mode=Timer.ONE_SHOT, period=period_start, callback=startAc)
    elif msg[0] == 'off' and not acOn:
        timer_light.init(mode=Timer.ONE_SHOT, period=period_start, callback=offAll)
    else:
        print("Error! Invalid command")
    
    if msg[0] == 'on':
        lightOn = True
    elif msg[0] == 'off':
        lightOn = False
    
def handleAll(msg):
    global acOn, lightOn
    
    period_start = int(msg[1]) * 1000
    
    try:
        timer_all.deinit()
    except:
        pass
    
    if msg[0] == 'on':
        timer_all.init(mode=Timer.ONE_SHOT, period=period_start, callback=startAll)
    elif msg[0] == 'off':
        timer_all.init(mode=Timer.ONE_SHOT, period=period_start, callback=offAll)
    else:
        print("Error! Invalid command")
        
    if msg[0] == 'on':
        acOn = True
        lightOn = True
    elif msg[0] == 'off':
        acOn = False
        lightOn = False
        
def handleMessage(status):
    if status:
        return b'On'
    else:
        return b'Off'

def sub_cb(msg_topic, msg_payload):
    global device, msg, change
    
    device = msg_topic
    msg = msg_payload
    
    change = True

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
    except:
        restart_and_reconnect()
    
    if change:
        msg = msg.decode('UTF-8').split(", ")
        
        if device == b'smarthome/ac':
            handleAc(msg)
        elif device == b'smarthome/light':
            handleLight(msg)
        elif device == b'smarthome/all':
            handleAll(msg)
            
        if (device == b'smarthome/ac') or (device == b'smarthome/all'):
            client.publish('smarthome/ac/status', handleMessage(acOn))
        if (device == b'smarthome/light') or (device == b'smarthome/all'):
            client.publish('smarthome/light/status', handleMessage(lightOn))

        change = False
