import time
import melopero_apds9960 as mp


def main():
    device = mp.APDS_9960()

    device.enable_proximity_engine()
    device.power_up()

    while True:
        time.sleep(.5)
        print(device.get_proximity_data())


if __name__ == "__main__":
    main()
