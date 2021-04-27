from serial import Serial, SerialException
from serial.tools import list_ports
from tkinter import Tk, Text, Entry, Button, INSERT, ttk, messagebox
from threading import Thread
from math import sqrt, acos, pi

# Gameboard and hand params
BOARD_LENGTH = 29
FIRST_SHOULDER = 22.5
SECOND_SHOULDER = 18
GRAB = 4.5
RADIUS_OF_HAND = 6.3
START_POSITION = {2: 65, 6: 130, 5: 75, 7: 90, 4: 20}

x_coord = [3, 6.5, 9.5, 13,
           16, 19.5, 23, 26]

y_coord = [3, 6, 9.5, 13,
           16, 19.5, 22.5, 26]


# Output of hand work states
def doubler():
    lastLine = ""
    while True:
        readLine = ser.readline()
        if readLine != lastLine:
            if readLine == b'Start!\r\n':
                output.insert(INSERT, readLine)
                output.see("end")
            elif readLine == b'1\r\n':
                output.insert(INSERT, "Выполняю команду \n")
                output.see("end")
            elif readLine == b'2\r\n':
                output.insert(INSERT, "*Готова принять координаты \n")
                output.see("end")
            elif readLine == b'3\r\n':
                output.insert(INSERT, "Команда успешно принята \n")
                output.see("end")
            elif readLine == b'4\r\n':
                output.insert(INSERT, "!Команда неверна! \n")
                output.see("end")
            else:
                output.insert(INSERT, readLine)
                output.see("end")
        lastLine = readLine


# Moving between 2 points
def send_serial_data(ser):
    x0, y0, x1, y1 = pointsInput.get().split()
    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)
    # Moving to first point
    dict1 = get_serv_values(x0, y0)
    transmit_data(ser, dict1)
    # Grabbing figure
    dict1[2] = 90
    transmit_data(ser, dict1)
    # Lifting the figure
    dict2 = dict1.copy()
    dict2[6] = 120
    transmit_data(ser, dict2)
    # Moving to secondd position and then moving to the start position
    dict3 = get_serv_values(x1, y1)
    dict3[2] = 90
    transmit_data(ser, dict3)
    transmit_data(ser, START_POSITION)


# Beating figure
def beating_figure(ser):
    x, y, x1, y1 = pointsInput.get().split()
    x, y, x1, y1 = float(x), float(y), float(x1), float(y1)
    #x, y, x1, y1 = 1.7 * x + 1.3, 1.7 * x + 1.1, 1.7 * x + 1.3, 1.7 * x + 1.1
    # Moving to the figure that should be beated
    dict1 = get_serv_values(x, y)
    transmit_data(ser, dict1)
    # Grabbing that figure
    dict1[2] = 90
    transmit_data(ser, dict1)
    # Lifting it
    dict2 = dict1.copy()
    dict2[6] = 140
    transmit_data(ser, dict2)
    # Removing the piece from a board
    vneDoski = {7: 0, 2: 90, 4: 30, 5: 120, 6: 80}
    transmit_data(ser, vneDoski)
    vneDoski[6] = 140
    vneDoski[2] = 65
    transmit_data(ser, vneDoski)
    # Move to the beating figure
    dict3 = get_serv_values(x1, y1)
    transmit_data(ser, dict3)
    # Grabbing it
    dict3[2] = 90
    transmit_data(ser, dict3)
    # Lifting
    dict4 = dict3.copy()
    dict4[6] = 140
    transmit_data(ser, dict4)
    # Moving to the place of the first
    transmit_data(ser, dict1)
    transmit_data(ser, START_POSITION)


# Calculation the angles of rotation of servos.
# alpha - angles of rotation of 6 servos.
# beta - angles of rotation of 5 servos.
# gamma - angles of rotation of 4 servos.
# delta - angles of rotation of 7 servos.
# length - distance between the beginning of the hand and the grip.
# distanceToPoint - distance between a point on the board and the end of the grapple.
def get_serv_values(x, y):
    flag = 0
    if x > BOARD_LENGTH / 2:
        flag = 1
    distanceToPoint = sqrt((BOARD_LENGTH / 2 - x) ** 2 +
                           (RADIUS_OF_HAND + y) ** 2)
    length = sqrt(distanceToPoint ** 2 + GRAB**2)
    try:
        alpha = acos((FIRST_SHOULDER ** 2 + length ** 2 - SECOND_SHOULDER ** 2) /
                     (2 * FIRST_SHOULDER * length)) + acos(distanceToPoint / length)
        beta = acos((FIRST_SHOULDER ** 2 + SECOND_SHOULDER ** 2 - length ** 2) /
                    (2 * FIRST_SHOULDER * SECOND_SHOULDER))
    except ValueError:
        message = "Out of acos/asin."
        messagebox.showerror("Ошибка", message)

    delta = 100 + acos((y + RADIUS_OF_HAND) / distanceToPoint) * 180 / pi
    if flag == 1:
        delta = 95 - acos((y + RADIUS_OF_HAND) / distanceToPoint) * 180 / pi


    alpha *= 180 / pi
    beta *= 180 / pi

    alpha, beta, delta = int(alpha), int(beta), int(delta)
    gamma = 270 - alpha - beta
    gamma -= 70    
    alpha += 20
    beta += 5
#    delta += 95
    """
    7, 8 servo
    if flag == 0:
        alpha += 8
        beta -= -2
        delta += 96
    if flag == 1:
        alpha += 0
        beta -= -6
        delta += 94
    """
    str2 = (str(alpha) + ", " + str(beta) + ", " + str(gamma) + ", " +
            str(delta) + "\n")
    output.insert(INSERT, str2)
    output.see("end")
    dictionary = {7: delta, 5: beta, 4: gamma, 6: alpha}
    return dictionary


# Transmition data to the Arduino
def transmit_data(ser, dictionary):
    keys = dictionary.keys()
    string = ""
    for key in keys:
        string += str(key) + "," + str(dictionary[key]) + ":"
    ser.write(string.encode('utf-8'))
    ser.flush()


# Sending 1 command to the Arduino in the following form: 'servo,angle'
def sendCommand(ser):
    string = commandInput.get()
    ser.write(string.encode('utf-8'))
    ser.flush()


# Creating the user interface
def createGUI():
    global output, pointsInput, commandInput, ser
    window = Tk()
    window.title("Robo")
    window.geometry('500x420')
    # COM ports of the PC
    ports = list_ports.comports()
    portLists = []
    for port, _, _ in sorted(ports):
        portLists.append(port)
    COMPorts = ttk.Combobox(window, values=portLists)
    COMPorts.grid(column=0, row=0)
    COMPorts.current(0)
    try:
        ser = Serial(port=COMPorts.get(), baudrate=9600)
    except SerialException:
        message = "Отказано в доступе при открытии COM-порта."
        messagebox.showerror("Ошибка", message)
    # Output textbox
    output = Text(window, width=30, height=20)
    output.grid(column=1, row=0, rowspan=7)
    # Points input textline
    pointsInput = Entry(window, width=20)
    pointsInput.grid(column=0, row=1)
    # Points sending button
    sendCoordinatesButton = Button(window, text="Send coordinates", width=20,
                                   command=lambda: send_serial_data(ser))
    sendCoordinatesButton.grid(column=0, row=2)
    # Figure beating button
    figureBeatingButton = Button(window, text="Beating figure", width=20,
                                 command=lambda: beating_figure(ser))
    figureBeatingButton.grid(column=0, row=3)
    # 1 command input textline
    commandInput = Entry(window, width=20)
    commandInput.grid(column=0, row=4)
    # Commands sending button
    sendCommandsButton = Button(window, text="Send command", width=20,
                                command=lambda: sendCommand(ser))
    sendCommandsButton.grid(column=0, row=5)
    # Returning to the start position button
    toStartButton = Button(window, text="To start position", width=20,
                           command=lambda: transmit_data(ser, START_POSITION))
    toStartButton.grid(column=0, row=6)
    my_thread = Thread(target=doubler)
    my_thread.start()
    window.mainloop()
    ser.close()

createGUI()
