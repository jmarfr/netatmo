# Netatmo

Script to collect data from netatmo api and send values to Promotheus exporter.

## Installation

````shell
git clone https://github.com/jmarfr/netatmo.git
cd netatmo
python3 -m venv .venv
source .venv/activate
pip install -r requirements.txt
python3 termostat.py
````

## Configuration

Environment variable are used for the moment. A futur version will use a configuration file.
Needed variables :

* **CLIENT_ID**: Netatmo API client id (Mandatory)
* **CLIENT_SECRET**: Netatmo API client name (Mandatory)
* **USERNAME**: Netatmo portal username (Mandatory)
* **PASSWORD**: Netatmo portal password (Mandatory)
* **TERMOSTAT_MAC**: MAC address of the termostat to check (Optional)
* **PROM_PUSH_GW**: Prometheus push gateway HOST:PORT (Optional)
* **PROM_PUSH_BATCH**: Prometheus batch name (Optional)
* **PROM_PUSH_INTERVAL**: Prometheus push interval in sec. Default to 60sec (Optional)
