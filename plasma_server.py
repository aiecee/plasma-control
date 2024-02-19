import wifi
import socketpool
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.headers import HTTPHeaders
from adafruit_httpserver.status import HTTPStatus
from neopixel_controller import NeoPixelController
import patterns

CONTROLLER_STATE = True
ON_STATE_MAIN = """
<section>
    <h2>Power</h2>
    <form action="/state" method="post">
        <button type="submit" name="state" value="on" disabled="disabled">On</button>
        <button type="submit" name="state" value="off">Off</button>
    </form>
</section>
<section>
    <h2>Control</h2>
    <form action="/brightness" method="post">
        <p>
            <label for="brightness">Brightness</label>
            <input type="number" name="brightness" value="0.5" min="0.1" max="1" step="0.1"/>
        </p>
        <button type="submit">Set</button>
    </form>
</section>
<section>
    <h2>Patterns</h2>
    <details>
        <summary>Fill</summary>
        <form action="/pattern" method="post">
            <p>
                <label for="color">Color</label>
                <input type="color" name="color" value="#ffffff"/>
            </p>
            <button type="submit" name="pattern" value="fill">Set</button>
        </form>
    </details>
    <details>
        <summary>Rainbow</summary>
        <form action="/pattern" method="post">
            <button type="submit" name="pattern" value="rainbow">Set</button>
        </form>
    </details>
    <details>
        <summary>Fade</summary>
        <form action="/pattern" method="post">
            <p>
                <label for="color">Color</label>
                <input type="color" name="color" value="#ffffff"/>
            </p>
            <p>
                <label for="speed">Speed</label>
                <input type="number" name="speed" value="0.01" min="0.01" max="0.1" step="0.01"/>
            </p>
            <button type="submit" name="pattern" value="fade">Set</button>
        </form>
    </details>
    <details>
        <summary>Twinkle</summary>
        <form action="/pattern" method="post">
            <p>
                <label for="color">Color</label>
                <input type="color" name="color" value="#ffffff"/>
            </p>
            <p>
                <label for="speed">Speed</label>
                <input type="number" name="speed" value="0.01" min="0.01" max="0.1" step="0.01"/>
            </p>
            <button type="submit" name="pattern" value="twinkle">Set</button>
        </form>
    </details>
</section>
"""
OFF_STATE_MAIN = """
<section>
    <h2>Power</h2>
    <form action="/state" method="post">
        <button type="submit" name="state" value="on">On</button>
        <button type="submit" name="state" value="off" disabled="disabled">Off</button>
    </form>
</section>
"""


def _webpage():
    html = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
        </head>
        <body>
            <header>
                <h1>Plasma Control</h1>
                <p>Brighten your world!</p>

            </header>
            <main>
                {ON_STATE_MAIN if CONTROLLER_STATE else OFF_STATE_MAIN}
            </main>
        </body
    </html>
    """
    return html


def _send_redirect(request: HTTPRequest):
    headers = HTTPHeaders({"Location": "/"})
    with HTTPResponse(
        request, status=HTTPStatus(303, "See Other"), headers=headers
    ) as response:
        response.send("")


def _read_form_data(request: HTTPRequest):
    form = {}
    body = request.body.decode("utf-8")
    chunks = body.split("&")
    for chunk in chunks:
        name, value = chunk.split("=")
        form[name] = value

    return form


def _hex_to_grb(value):
    hex_code = value.strip("%23")
    rgb = tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
    return (rgb[1], rgb[0], rgb[2])


def build(hostname, ssid, password, controller: NeoPixelController):
    wifi.radio.hostname = hostname
    wifi.radio.connect(ssid, password)
    pool = socketpool.SocketPool(wifi.radio)
    server = HTTPServer(pool)

    @server.route("/")
    def index(request: HTTPRequest):
        with HTTPResponse(
            request,
            content_type=MIMEType.TYPE_HTML,
        ) as response:
            response.send(f"{_webpage()}")

    @server.route("/state", HTTPMethod.POST)
    def state(request: HTTPRequest):
        global CONTROLLER_STATE
        form = _read_form_data(request)
        if form["state"] == "on":
            CONTROLLER_STATE = True
            controller.set_pattern(patterns.fill((255, 255, 255)))
        if form["state"] == "off":
            CONTROLLER_STATE = False
            controller.set_pattern(patterns.fill((0, 0, 0)))

        _send_redirect(request)

    @server.route("/brightness", HTTPMethod.POST)
    def brightness(request: HTTPRequest):
        if not CONTROLLER_STATE:
            _send_redirect(request)
            return

        form = _read_form_data(request)
        controller.set_brightness(float(form["brightness"]))

        _send_redirect(request)

    @server.route("/color", HTTPMethod.POST)
    def color(request: HTTPRequest):
        if not CONTROLLER_STATE:
            _send_redirect(request)
            return

        form = _read_form_data(request)
        grb = _hex_to_grb(form["color"])
        controller.set_pattern(patterns.fill(grb))

        _send_redirect(request)

    @server.route("/pattern", HTTPMethod.POST)
    def pattern(request: HTTPRequest):
        if not CONTROLLER_STATE:
            _send_redirect(request)
            return

        form = _read_form_data(request)
        if form["pattern"] == "rainbow":
            controller.set_pattern(patterns.rainbow)

        if form["pattern"] == "fade":
            grb = _hex_to_grb(form["color"])
            speed = float(form["speed"])
            controller.set_pattern(patterns.fade(grb, speed))

        if form["pattern"] == "fill":
            grb = _hex_to_grb(form["color"])
            controller.set_pattern(patterns.fill(grb))

        if form["pattern"] == "twinkle":
            grb = _hex_to_grb(form["color"])
            speed = float(form["speed"])
            controller.set_pattern(patterns.twinkle(grb, speed))

        _send_redirect(request)

    server.start(str(wifi.radio.ipv4_address))
    print(f"Server started at http://{wifi.radio.ipv4_address}:80")
    return server
