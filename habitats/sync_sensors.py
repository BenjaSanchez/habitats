from habitats.aqara import get_sensors
from habitats.database import update_sensors


def main():
    sensors = get_sensors()

    if not sensors:
        raise RuntimeError("No Aqara temperature/humidity sensors found.")

    update_sensors(sensors)

    print(f"Synchronized {len(sensors)} sensors:")
    for sensor in sensors:
        print(f"  {sensor['name']} ({sensor['device_id']})")


if __name__ == "__main__":
    main()
