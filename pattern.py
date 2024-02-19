import time


class Pattern:
    def __init__(self, name):
        self.name = name

    def run(self, pixels, speed):
        pass


class Fill(Pattern):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def run(self, pixels, speed):
        for i in range(pixels.n):
            pixels[i] = self.color
        pixels.show()
        time.sleep(speed)
