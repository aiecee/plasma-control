from neopixel import NeoPixel
from patterns import fill


class NeoPixelController:
    def __init__(self, pin, num_pixels: int, brightness: float = 0.5):
        self._pixels = NeoPixel(pin, num_pixels, auto_write=False)
        self._pixels.brightness = brightness
        self._pattern = fill((255, 255, 255))

    def set_brightness(self, brightness: float):
        self._pixels.brightness = brightness

    def set_pattern(self, pattern):
        self._pattern = pattern

    def run(self, speed: float):
        self._pattern(self._pixels, speed)
