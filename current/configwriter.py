from configparser import ConfigParser
from configparser import ConfigParser

config = ConfigParser()

config["worker1"] = {
    "hostname": "broker1.local",
    "plain_port": "9093"
}

config["broker2"] = {
    "hostname": "broker2.local",
    "plain_port": "9093"
}

config["broker3"] = {
    "hostname": "broker3.local",
    "plain_port": "9093"
}

config["worker1"] = {
    "port": "8083",
    "connector": "cdc-oracle-reader1"
}

config["worker2"] = {
    "port": "8084",
    "connector": "cdc-oracle-reader2"
}

config["worker3"] = {
    "port": "8085",
    "connector": "cdc-oracle-reader3"
}

config["worker4"] = {
    "port": "8086",
    "connector": "cdc-oracle-reader4"
}

config["worker5"] = {
    "port": "8087",
    "connector": "cdc-oracle-reader5"
}

with open("config.ini", "w") as f:
    config.write(f)