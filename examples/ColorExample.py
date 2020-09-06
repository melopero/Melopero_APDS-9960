import time
import melopero_apds9960 as mp


def main():
    device = mp.APDS_9960()

    device.reset()

    device.enable_als_engine()
    device.set_als_integration_time(200)
    device.power_up()

    while True:
        time.sleep(.5)
        print(device.get_color_data())


if __name__ == "__main__":
    main()
