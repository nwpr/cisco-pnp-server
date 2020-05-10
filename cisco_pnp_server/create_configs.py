import os

CONFIG_DIR = "configs/"

DEVICES = {
    "9DNVJ6W5CFV": {
        "base-config": "base.config",
        "vars": {
            "ip1": "10.10.10.10",
            "snm1": "255.255.255.0"
        }
    }
}


def run():
    for device in DEVICES.items():
        create_config(device)


def create_config(device):
    serial, device = device
    with open(os.path.join(CONFIG_DIR, device["base-config"]), 'r') as file:
        config = file.read()
    if "vars" in device:
        config = config.format(**device["vars"])
    with open(os.path.join(CONFIG_DIR, serial + ".config"), "w+") as file:
        file.write(config)
    print(serial, device)


if __name__ == '__main__':
    run()
