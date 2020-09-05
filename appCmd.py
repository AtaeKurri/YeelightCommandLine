import argparse, yeelight, json

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("ip", type=str, help="Tells the program what bulb to control.")
    parse.add_argument("-p", "--power", help="trigger the power state.", choices=["on", "off"])
    parse.add_argument("-b", "--brightness", type=int, help="Set the brightness to a percentage value.")
    parse.add_argument("-T", "--temp", type=int, help="Set the color temperature.")
    parse.add_argument("-c", "--rgb", type=int, help="Set a color from the rgb format.", nargs=3)
    parse.add_argument("-n", "--name", type=str, help="Set the bulb's name")
    parse.add_argument("-d", "--discover", action='store_true', help="Show the full list of yeelight bulbs in your network.")
    parse.add_argument("-t", "--toggle", action='store_true')
    args = parse.parse_args()
    global bulb

    try:
        # Connect with ip to the given bulb.
        try:
            bulb = yeelight.Bulb(args.ip)
        except:
            try:
                for bulbs in yeelight.discover_bulbs():
                    if args.ip in bulbs["capabilities"]["name"]:
                        bulb = yeelight.Bulb(bulbs["ip"])
            except:
                print("Bulb not found.")
        
        # Arguments handeling
        if args.power: # Bulb powering on/off
            turn_power(args.power)

        if args.brightness:
            bulb.set_brightness(args.brightness)

        if args.temp:
            bulb.set_color_temp(args.temp)

        if args.rgb:
            rbg = args.rgb
            bulb.set_rgb(rgb[0], rgb[1], rgb[2])

        if args.name:
            bulb.set_name(args.name)

        if args.discover:
            with open("discover.txt", 'w') as f:
                json.dump(yeelight.discover_bulbs(), f, indent=2)

        if args.toggle:
            bulb.toggle()
    except:
        print("IP field needed.")

def turn_power(state):
    if state == "on":
        bulb.turn_on()
    elif state == "off":
        bulb.turn_off()

if __name__ == '__main__':
    main()