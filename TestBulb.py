# An Accessory for a LED attached to pin 11.
import logging
from sched import scheduler
from threading import Thread

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

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

radio.begin()
time.sleep(0.1)
network.begin(90, this_node)

schedule = scheduler(time.time, time.sleep)

def runner():
    while True:
        try:
            schedule.run()
        except:
            pass

myThread = Thread(target=runner)
myThread.start()

class LightBulb(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, *args, pin=11, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_bulb)

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_bulb(self, value):
        def my_action():
            payload = None
            if value:
                payload = pack('<B', 1)
            else:
                payload = pack('<B', 0)
            network.write(RF24NetworkHeader(other_node), payload)
        schedule.enter(0, 0, my_action)

    def stop(self):
        super().stop()