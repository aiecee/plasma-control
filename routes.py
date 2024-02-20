from adafruit_httpserver import Request, Response
from adafruit_templateengine import render_template
from led_controller import LEDController
from patterns import rainbow, fill, fade, twinkle


def _read_form_data(request: Request):
    form = {}
    body = request.body.decode("utf-8")
    chunks = body.split("&")
    for chunk in chunks:
        name, value = chunk.split("=")
        form[name] = value

    return form


def _hex_to_grb(value):
    hex_color = value[3:]
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return (rgb[1], rgb[0], rgb[2])


def index(controller: LEDController):
    def _index(request: Request):
        page_context = {
            "power_state": controller.power_state,
            "current_brightness": controller.brightness(),
        }
        rendererd = render_template("templates/page.tpl.html", page_context)
        return Response(request, rendererd, content_type="text/html")

    return _index


def power(controller: LEDController):
    def _power(request: Request):
        form_data = _read_form_data(request)
        if form_data["state"] == "on":
            controller.on()
        if form_data["state"] == "off":
            controller.off()

        power_state_context = {
            "power_state": controller.power_state,
            "current_brightness": controller.brightness(),
        }
        rendererd = render_template(
            "templates/power.tpl.html",
            power_state_context,
        )
        return Response(request, rendererd, content_type="text/html")

    return _power


def brightness(controller: LEDController):
    def _brightness(request: Request):
        form_data = _read_form_data(request)
        brightness = float(form_data["brightness"])
        controller.set_brightness(brightness)
        brightness_context = {"current_brightness": controller.brightness()}
        rendererd = render_template("templates/brightness.tpl.html", brightness_context)
        return Response(request, rendererd, content_type="text/html")

    return _brightness


def pattern(controller: LEDController):
    def _pattern(request: Request):
        form_data = _read_form_data(request)

        if form_data["pattern"] == "rainbow":
            controller.set_pattern(rainbow)
        if form_data["pattern"] == "fill":
            grb = _hex_to_grb(form_data["color"])
            controller.set_pattern(fill(grb))
        if form_data["pattern"] == "fade":
            grb = _hex_to_grb(form_data["color"])
            speed = float(form_data["speed"])
            controller.set_pattern(fade(grb, speed))
        if form_data["pattern"] == "twinkle":
            grb = _hex_to_grb(form_data["color"])
            speed = float(form_data["speed"])
            controller.set_pattern(twinkle(grb, speed))
        return Response(request, "")

    return _pattern
