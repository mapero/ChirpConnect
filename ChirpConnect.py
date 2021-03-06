import Chirp, getopt
import paho.mqtt.client as mqtt
import sys, time
import logging

class ChirpConnect:
    def __init__(self, bus=1, addr=0x20, host="localhost", port=2337, ssl=True, topic="sensors/Chirp", interval=60):
        self.bus_num = bus
        self.bus_addr = addr
        self.mqtt_host = host
        self.mqtt_port = port
        self.mqtt_ssl = ssl
        self.mqtt_topic = topic
        self.interval = interval
        self.chirp = Chirp.Chirp(self.bus_num, self.bus_addr)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish    
        logging.basicConfig(level=logging.DEBUG)

    
    def on_connect(self, client, userdata, flag, rc):
        logging.info("Connected with result code" + str(rc))
        
    def on_publish(self, client, userdata, mid):
        logging.debug("Message " + str(mid) + "published to topic")
    
    def publishTemp(self):
        temp = self.chirp.temp()
        logging.debug("Publishing " + self.mqtt_topic +"/temp with value: " +str(temp))
        rc = self.client.publish(self.mqtt_topic + "/temp", temp, 0, False)
        logging.debug(str(rc))
    
    def publishMoisture(self):
        moisture = self.chirp.cap_sense()
        logging.debug("Publishing " + self.mqtt_topic +"/moisture with value: " +str(moisture))
        rc = self.client.publish(self.mqtt_topic + "/moisture", moisture, 0, False)
        logging.debug(str(rc))
        
    def publishLight(self):
        light = self.chirp.light()
        logging.debug("Publishing " + self.mqtt_topic +"/light with value: "+str(light))
        rc = self.client.publish(self.mqtt_topic + "/light", light, 0, False)
        logging.debug(str(rc))
        
    def loop(self):
        logging.info("Connecting to "+self.mqtt_host+" on port "+ str(self.mqtt_port))
        self.client.connect(self.mqtt_host, self.mqtt_port, 60, "")
        self.client.loop_start()
        starttime = time.time()
        try:
            while(True):
                self.publishLight()
                self.publishMoisture()
                self.publishTemp()
                time.sleep(self.interval - ((time.time()-starttime) % self.interval))
        except KeyboardInterrupt:
            pass
        self.client.disconnect()
        logging.info("Exiting")
        
def printOpt():
    print "ChirpConnect -b <bus=1> -a <address=0x20> -h <host=localhost> -p <port=2337> --ssl -t <topic=sensors/Chirp> -i <interval=60>"

def main(argv):
    bus = 1
    address = 0x20
    host = "localhost"
    port = 2337
    ssl = False
    topic = "sensors/Chirp"
    interval = 60
    
    try:
        opts, args = getopt.getopt(argv, "b:a:h:p:t:i:", ["ssl"])
    except getopt.GetoptError:
       printOpt()
       sys.exit(2)
    for opt, arg in opts:
        if opt == "-b":
            bus = int(arg)
        elif opt == "-a":
            address = int(arg)
        elif opt == "-h":
            host = arg
        elif opt == "-p":
            port = int(arg)
        elif opt == "--ssl":
            ssl=True
        elif opt == "-t":
            topic = arg
        elif opt == "-i":
            interval = int(arg)
    chirpConnect = ChirpConnect(bus, address, host, port, ssl, topic, interval)
    chirpConnect.loop()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    
    
