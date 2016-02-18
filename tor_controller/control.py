import socket
import time
from .excepts import *
from .utils import *


class Tor:
    def __init__(self, host="127.0.0.1", port=9051):
        self.host, self.port = host, port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._auth_method = None

    def connect(self):
        try:
            self._socket.connect((self.host, self.port))
            self._auth()
        except socket.error as err:
            raise ConnectionError(err.message)

    def _auth(self):
        try:
            if self._auth_method == None:
                # TODO: get password from cli
                password = '"password"'
                auth_string = "authenticate " + password + " \r\n"
                self._socket.send(auth_string.encode("UTF-8"))
            else:
                raise TorError("No authentication method")

            if self._socket.recv(1024).decode("UTF-8").rstrip() != "250 OK":
                raise TorError("Failed to authenticate")
        except socket.error as err:
            raise ConnectionError(err.message)

    def close(self):
        self._send("QUIT\r\n")
        self._socket.close()

    def _send(self, data):
        try:
            self._socket.send(data.encode("UTF-8"))
            return self._socket.recv(1024).decode("UTF-8").rstrip()
        except socket.error as err:
            raise ConnectionError(err.message)

    def getinfo(self, option):
        status = self._send("getinfo %s\r\n" % option)
        time.sleep(0.2)
        return status

    def closecircuit(self, number):
        status = self._send("closecircuit %s\r\n" % number)
        # if code(status) != "250":
        #     raise TorError(status)
        return status

    def extendcircuit(self, number):
        status = self._send("extendcircuit %s\r\n" % number)
        if code(status) != "250":
            raise TorError(status)
        return status


