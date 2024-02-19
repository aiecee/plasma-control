import os
import time
import board
import microcontroller
from neopixel_controller import NeoPixelController
import plasma_server

controller = NeoPixelController(board.GP15, 50)
try:
    server = plasma_server.build(
        "PicoPlasma", os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"), controller
    )
except OSError:
    print("Error starting server...")
    print("Restarting in 5 secs....")
    time.sleep(5)
    microcontroller.reset()


while True:
    controller.run(0)
    server.poll()
