import time
import melopero_apds9960 as mp


def main():
    device = mp.APDS_9960()

    device.reset()

    device.enable_als_engine()
    device.set_als_integration_time(450)
    saturation = device.get_saturation()
    device.power_up()

    while True:
        time.sleep(.5)
        color = device.get_color_data()
        color = map(lambda val : val / saturation * 255, color)
        print(f"Clear: {color[0]}  Red: {color[1]}  Green: {color[2]}  Blue: {color[3]}")


if __name__ == "__main__":
    main()
