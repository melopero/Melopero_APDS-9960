import time
import melopero_apds9960 as mp


def main():
    device = mp.APDS_9960()

    device.reset()

    device.enable_als_engine()
    device.set_als_integration_time(450)
    saturation = device.get_saturation() * 255
    device.power_up()

    while True:
        time.sleep(.5)
        color = device.get_color_data()
        print(f"Clear: {color[0] /saturation}  Red: {color[1] / saturation}  Green: {color[2] / saturation}  Blue: {color[3] /saturation}")


if __name__ == "__main__":
    main()
