import redrat
import time
import socket

class RemoteControl(object):

    def press(self, key):
        raise NotImplementedError()

    def keydown(self, key):
        raise NotImplementedError()

    def keyup(self, key):
        raise NotImplementedError()

    def keydelay(self, key):
        raise NotImplementedError()

class IRRedRatControl(RemoteControl):

    def __init__(self, hostname, port, output, config):
        self.hostname = hostname
        self.port = int(port or 10001)
        self.output = int(output)
        self.config = redrat.RemoteControlConfig(config)
        with self._connect() as irnb:
            irnb.power_on()
        time.sleep(0.5)


    def press(self, key):
        with self._connect() as irnb:
            irnb.irsend_raw(
                port=self.output, power=100, data=self.config[key])


    def _connect(self):
        try:
            return irnetbox.IRNetBox(self.hostname, self.port)
        except socket.error as e:
            e.args = (("Failed to connect to IRNetBox %s: %s" % (
                self.hostname, e)),)
            e.strerror = e.args[0]
            raise
    def _KEYMAP = {
        "KEY_HOME": 01,
        "KEY_REWIND": 02,
        "KEY_FASTFORWARD": 03,
        "KEY_PLAY": 04,
        "KEY_PAUSE": 05,
'''
        Key value mapping from radrat
'''
    }

class HttpControl(object):

    _KEYNAMES = {
        "KEY_HOME": "Home",
        "KEY_REWIND": "Rev",
        "KEY_FASTFORWARD": "Fwd",
        "KEY_PLAY": "Play",
        "KEY_PAUSE": "Play",
        "KEY_PLAYPAUSE": "Play",
        "KEY_OK": "Select",
        "KEY_LEFT": "Left",
        "KEY_RIGHT": "Right",
        "KEY_DOWN": "Down",
        "KEY_UP": "Up",
        "KEY_BACK": "Back",
        "KEY_AGAIN": "InstantReplay",
        "KEY_INFO": "Info",
        "KEY_BACKSPACE": "Backspace",
        "KEY_SEARCH": "Search",
        "KEY_ENTER": "Enter",
        "KEY_VOLUMEDOWN": "VolumeDown",
        "KEY_MUTE": "VolumeMute",
        "KEY_VOLUMEUP": "VolumeUp",
        "KEY_EPG": "TV Guide",
    }

    def __init__(self, hostname, timeout_secs=3):
        self.hostname = hostname
        self.timeout_secs = timeout_secs

    def press(self, key):
        import requests

        keyname = self._KEYNAMES.get(key, key)
        response = requests.post(
            "http://%s:8060/keypress/%s" % (self.hostname, keyname),
            timeout=self.timeout_secs)
        response.raise_for_status()
        debug("Pressed " + key)

    def keydown(self, key):
        import requests

        keyname = self._KEYNAMES.get(key, key)
        response = requests.post(
            "http://%s:8060/keydown/%s" % (self.hostname, keyname),
            timeout=self.timeout_secs)
        response.raise_for_status()
        debug("Holding " + key)

    def keyup(self, key):
        import requests

        keyname = self._KEYNAMES.get(key, key)
        response = requests.post(
            "http://%s:8060/keyup/%s" % (self.hostname, keyname),
            timeout=self.timeout_secs)
        response.raise_for_status()
        debug("Released " + key)
