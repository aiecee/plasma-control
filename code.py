import os
import time
import microcontroller
import board
from adafruit_httpserver import Route, GET, POST
from server import ServerBuilder
from led_controller import LEDController
from routes import index, power, brightness, pattern


controller = LEDController(board.GP15, 50)
try:
    ip_address = os.getenv("IP_ADDRESS")

    http_server = (
        ServerBuilder()
        .set_ssid(os.getenv("WIFI_SSID"))
        .set_password(os.getenv("WIFI_PASSWORD"))
        .set_static_ip(
            os.getenv("IP_ADDRESS"), os.getenv("NETMASK"), os.getenv("GATEWAY")
        )
        .build()
    )
    http_server.add_routes(
        [
            Route("/", [GET], index(controller)),
            Route("/power", [POST], power(controller)),
            Route("/brightness", [POST], brightness(controller)),
            Route("/pattern", [POST], pattern(controller)),
        ]
    )
    http_server.start(ip_address)
except Exception as e:
    print("An error occured:", e)
    print("Restarting in 5 secs....")
    time.sleep(5)
    microcontroller.reset()


while True:
    controller.run(0)
    http_server.poll()
