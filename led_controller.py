from neopixel import NeoPixel
from microcontroller import Pin
from patterns import fill


class LEDController:
    def __init__(self, pin: Pin, num_pixels: int):
        self.power_state = False
        self._off_pattern = fill((0, 0, 0))
        self._pixels = NeoPixel(pin, num_pixels, auto_write=False)
        self._pixels.brightness = 0.5
        self._pattern = fill((255, 255, 255))

    def set_brightness(self, brightness: int):
        self._pixels.brightness = brightness / 10

    def brightness(self):
        return self._pixels.brightness * 10

    def on(self):
        self.power_state = True

    def off(self):
        self.power_state = False

    def set_pattern(self, pattern):
        self._pattern = pattern

    def run(self, speed: float):
        if self.power_state:
            self._pattern(self._pixels, speed)
        else:
            self._off_pattern(self._pixels, speed)
