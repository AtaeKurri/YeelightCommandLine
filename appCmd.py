import argparse, yeelight, json

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--ip", type=str, help="Tells the program what bulb to control.")
    parse.add_argument("-p", "--power", help="trigger the power state.", choices=["on", "off"])
    parse.add_argument("-b", "--brightness", type=int, help="Set the brightness to a percentage value.")
    parse.add_argument("-T", "--temp", type=int, help="Set the color temperature.")
    parse.add_argument("-c", "--rgb", type=int, help="Set a color from the rgb format.", nargs=3)
    parse.add_argument("-n", "--name", type=str, help="Set the bulb's name")
    parse.add_argument("-d", "--discover", action='store_true', help="Show the full list of yeelight bulbs in your network.")
    parse.add_argument("-t", "--toggle", action='store_true')
    args = parse.parse_args()
    global bulb

    # Connect with ip to the given bulb.
    if args.ip: bulb = yeelight.Bulb(args.ip)
    else:
        found = False
        for bulbs in yeelight.discover_bulbs():
                bulb = yeelight.Bulb(bulbs["ip"])
                found = True
        if not found:
            print("Bulb not found.")
        
    # Arguments handeling
    if args.power: # Bulb powering on/off
        turn_power(args.power)

    if args.brightness: # Bulb brightness percentage
        bulb.set_brightness(args.brightness)

    if args.temp: # Color temperature
        bulb.set_color_temp(args.temp)

    if args.rgb: # Color rgb
        rbg = args.rgb
        bulb.set_rgb(rgb[0], rgb[1], rgb[2])

    if args.name: # Set bulb nickname (can be seen in the official mobile software too)
        bulb.set_name(args.name)

    if args.discover: # Create a file with informations on all the bulbs in the network
        with open("discover.txt", 'w') as f:
            json.dump(yeelight.discover_bulbs(), f, indent=2)

    if args.toggle: # Power toggle
        bulb.toggle()

def turn_power(state):
    if state == "on":
        bulb.turn_on()
    elif state == "off":
        bulb.turn_off()

if __name__ == '__main__':
    main()