import time
from struct import *
from RF24 import *
from RF24Network import *

radio = RF24(RPI_V2_GPIO_P1_15, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ)
network = RF24Network(radio)

millis = lambda: int(round(time.time() * 1000))
octlit = lambda n:int(n, 8)

# Address of our node in Octal format (01, 021, etc)
this_node = octlit("00")

# Address of the other node
other_node = octlit("01")

interval = 2000

radio.begin()
time.sleep(0.1)
network.begin(90, this_node)    # channel 90
radio.printDetails()
packets_sent = 0
last_sent = 0

while 1:
    network.update()
    now = millis()
    # If it's time to send a message, send it!
    if ( now - last_sent >= interval  ):
        last_sent = now
        print('Sending ..')
        payload = pack('<B', 1)
        packets_sent += 1
        ok = network.write(RF24NetworkHeader(other_node), payload)
        if ok:
            print('ok.')
        else:
            print('failed.')
