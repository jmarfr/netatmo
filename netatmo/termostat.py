from . import Netatmo
import requests
import logging

logging.getLogger(__name__)


class Termostat(Netatmo):
    def __init__(self, client_id, client_secret, username, password):
        self.home_id = None
        self.room_id = None
        super().__init__(client_id, client_secret, username, password, scope="read_thermostat")

    def read_termostat_status(self, home_name, room_name, termostat_mac_address=None):
        """Read Termostat values"""

        self._get_home_infos(home_name, room_name)
        headers = {
            "Authorization": f"Bearer {self._access_token}"
        }
        r = requests.get(f"{self.base_url}/api/homestatus?home_id={self.home_id}&device_types=NATherm1", headers=headers)
        r.raise_for_status()
        resp = r.json()

        termostat_modules = list()
        termostat_status = dict()

        # Modules in room
        for module in resp['body']['home']['modules']:
            if module['type'] == "NATherm1":
                if termostat_mac_address is None:
                    termostat_modules.append(module)
                else:
                    if module["id"] == termostat_mac_address:
                        termostat_modules.append(module)
                    else:
                        continue

        # Room informations
        for room in resp['body']['home']['rooms']:
            if room['id'] == self.room_id:
                room['name'] = room_name
                termostat_status = room

        return termostat_status, termostat_modules

    def _get_home_infos(self, home_name, room_name):
        """Get Home id from Name"""

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._access_token}"
        }

        r = requests.get("https://api.netatmo.com/api/homesdata?gateway_types=NATherm1", headers=headers)
        r.raise_for_status()
        resp = r.json()
        homes = resp['body']['homes']
        for home in homes:
            if home['name'] == home_name:
                logging.debug("Found home %s", home['name'])
                self.home_id = home["id"]
                for room in home["rooms"]:
                    if room['name'] == room_name:
                        logging.debug("Found room %s", room['name'])
                        self.room_id = room['id']
        if self.home_id is None or self.room_id is None:
            raise ValueError("home_id or room_id not found")
        return self.home_id, self.room_id


