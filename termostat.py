#! /usr/bin/env python3

import logging
import os

from prometheus_client import Gauge, Info, push_to_gateway, CollectorRegistry
from time import sleep
from netatmo.termostat import Termostat

if __name__ == "__main__":

    while True:
        try:
            logging.basicConfig(level=logging.DEBUG)

            netatm = Termostat(client_id=os.environ.get("CLIENT_ID"),
                               client_secret=os.environ.get("CLIENT_SECRET"),
                               username=os.environ.get("USERNAME"),
                               password=os.environ.get("PASSWORD"))

            term_modules, term_status = netatm.read_termostat_status("Maison",
                                                                     "Salon",
                                                                     termostat_mac_address=os.environ.get("TERMOSTAT_MAC")
                                                                     )
            logging.debug(term_modules)
            logging.debug(term_status)

            registry = CollectorRegistry()

            therm_measured_temperature = Gauge("therm_measured_temperature", "Measured temperature", ['id', 'name'],
                                               registry=registry)
            therm_measured_temperature.labels(id=term_modules['id'], name=term_modules['name']).set(
                term_modules['therm_measured_temperature'])
            # therm_measured_temperature.set_to_current_time()

            heating_power_request = Gauge("heating_power_request", "Heating power request", ['id', 'name'], registry=registry)
            heating_power_request.labels(id=term_modules['id'], name=term_modules['name']).set(
                term_modules['heating_power_request'])
            # heating_power_request.set_to_current_time()

            therm_setpoint_temperature = Gauge("therm_setpoint_temperature", "Thermostat setpoint temperature", ['id', 'name'],
                                               registry=registry)
            therm_setpoint_temperature.labels(id=term_modules['id'], name=term_modules['name']).set(
                term_modules['therm_setpoint_temperature'])
            # therm_setpoint_temperature.set_to_current_time()

            infos = Info("room_info", "Room informations", ['id'], registry=registry)
            infos.labels(id=term_modules['id']).info({'anticipating': str(term_modules['anticipating']),
                                                                                 'name': term_modules['name'],
                                                                                 'therm_setpoint_mode': term_modules[
                                                                                 'therm_setpoint_mode']})

            push_to_gateway(os.environ.get("PROM_PUSH_GW", "localhost:9091"),
                            os.environ.get("PROM_PUSH_BATCH", "Netatmo"),
                            registry=registry,
                            )

            sleep(os.environ.get("PROM_PUSH_INTERVAL", 60))
        except KeyboardInterrupt:
            print("\n\nKeyboard interuption received. Exiting.")
            exit()
