import Chirp, getopt
import paho.mqtt.client as mqtt
import sys, time

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

    
    def on_connect(self, client, userdata, flag, rc):
        print("Connected with result code" + str(rc))
    
    def publishTemp(self):
        self.client.publish(self.mqtt_topic + "temp", self.chirp.temp(), 0, False)
    
    def publishMoisture(self):
        self.client.publish(self.mqtt_topic + "moisture", self.chirp.cap_sense(), 0, False)
        
    def publishLight(self):
        self.client.publish(self.mqtt_topic + "light", self.chirp.light(), 0, False)
        
    def loop(self):
        self.client.connect(self.mqtt_host, self.mqtt_port, 60, "")
        self.client.loop()
        starttime = time.time()
        while(True):
            self.publishLight()
            self.publishMoisture()
            self.publishTemp()
            time.sleep(self.interval - ((time.time()-starttime) % self.interval))
        
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
        opts, args = getopt.getopt(argv, "bahpti", ["ssl"])
    except getopt.GetoptError:
       printOpt()
       sys.exit(2)
    for opt, arg in opts:
        if opt == "-b":
            bus = arg
        elif opt == "-a":
            address = arg
        elif opt == "-h":
            host = arg
        elif opt == "-p":
            port = arg
        elif opt == "--ssl":
            ssl=True
        elif opt == "-t":
            topic = arg
        elif opt == "-i":
            interval = arg
    chirpConnect = ChirpConnect(bus, address, host, port, ssl, topic, interval)
    chirpConnect.loop()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    
    
