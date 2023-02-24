from serial.tools import list_ports


def serialSelect(searchString):
    # check if there is a serial port with the given search string
    # if there are multiple matches, ask the user to select one
    # return the selected port
    # if no port found, print error and exit

    serialPorts = list(list_ports.comports())
    ports = []
    for port in serialPorts:
        if searchString in port[1]:
            ports.append(port[0])
    if len(ports) == 0:
        print("No serial port found with search string: " + searchString)
        print("Exiting...")
        exit()
    elif len(ports) == 1:
        return ports[0]
    else:
        print("Multiple serial ports found:")
        for i in range(len(ports)):
            print(str(i) + ": " + ports[i])
        return ports[int(input())]

if __name__ == "__main__":
    print(serialSelect(input("Serial Port Search String: ")))
