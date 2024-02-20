import wifi
import socketpool
from ipaddress import IPv4Address
from adafruit_httpserver import Server


class ServerBuilder:
    def __init__(self):
        self._hostname = None
        self._ssid = None
        self._password = None
        self._ipv4 = None
        self._netmask = None
        self._gateway = None

    def set_hostname(self, hostname: str):
        self._hostname = hostname
        return self

    def set_ssid(self, ssid: str):
        self._ssid = ssid
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def set_static_ip(self, ip_address: str, netmask: str, gateway: str):
        self._ipv4 = ip_address
        self._netmask = netmask
        self._gateway = gateway
        return self

    def build(self):
        if not all((self._ssid, self._password)):
            raise ValueError("One or more required fields are missing")

        if (
            self._ipv4 is not None
            and self._netmask is not None
            and self._gateway is not None
        ):
            wifi.radio.set_ipv4_address(
                ipv4=IPv4Address(self._ipv4),
                netmask=IPv4Address(self._netmask),
                gateway=IPv4Address(self._gateway),
            )

        wifi.radio.hostname = (
            self._hostname if self._hostname is not None else "PicoPlasma"
        )

        wifi.radio.connect(self._ssid, self._password)
        pool = socketpool.SocketPool(wifi.radio)
        server = Server(pool)
        return server
