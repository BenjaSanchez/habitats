from habitats.aqara import get_sensor_readings
from habitats.database import get_active_sensors, insert_readings


def main():
    sensors = get_active_sensors()

    if not sensors:
        raise RuntimeError("No active sensors found in D1.")

    readings = get_sensor_readings(sensors)

    if not readings:
        raise RuntimeError("Aqara returned no sensor readings.")

    insert_readings(readings)

    print(f"Collected readings for {len(readings)} sensors.")

    for reading in readings:
        print(
            f"  {reading['device_id']}: "
            f"{reading['temperature']} °C, "
            f"{reading['humidity']} %"
        )


if __name__ == "__main__":
    main()
