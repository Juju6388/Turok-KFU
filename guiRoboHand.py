import serial
from tkinter import *
from tkinter import scrolledtext
import threading
from threading import Thread
from math import *


def sendSerialData(ser):
    x, y = txt2.get().split()
    try:
        ser.write(bytes(txt2.get().encode()))
        txt.insert(INSERT, f'{ser.readline().strip()}\n')
        ser.flush()  # Buffer for stack command
    except SerialException:
        print('error')


# def Obrabotka(a=10.5, b=9, c=11.5, d=12):
#     l = sqrt(d * d + c * c)
#     alpha = int((acos((a * a + l * l - b * b) / (2 * a * l)) + acos(d / l)) * 180 / pi)
#     beta = int((acos((a * a + b * b - l * l) / (2 * a * b))) * 180 / pi)
#     gamma = 270 - alpha - beta
#     str2 = str(alpha) + ", " + str(beta) + ", " + str(gamma)
#     txt.insert(INSERT, str2)


def Transmit():
    set_ser.close()
    set_ser.open()
    set_ser.write(txt2.get())
    str3 = ""
    while str3 == "":
        str3 = set_ser.read(1)
    txt.insert(INSERT, str3)


def closePort(ser):
    txt.insert(INSERT, 'Port is closed')
    ser.close()


def createGUI(ser):
    global txt, txt2
    window = Tk()
    window.title("Robo")
    window.geometry('550x550')
    lbl = Label(window, text="Проверка состояния руки", font=("Arial", 12))
    lbl.grid(column=1, row=0, padx=20, sticky=NW)
    txt = scrolledtext.ScrolledText(window, width=30, height=20)
    txt.grid(column=1, row=1, rowspan=7, padx=20, sticky=N)
    txt2 = Entry(window, width=10)
    txt2.grid(column=0, row=0)  # txt.get()
    btn = Button(window, text="Отправить данные", command=lambda: sendSerialData(ser))
    btn.grid(column=0, row=1, sticky=NW)
    btn2 = Button(window, text="Выключить компорт", command=lambda: closePort(ser))
    btn2.grid(column=2, row=1, sticky=NW)
    window.mainloop()


ser = serial.Serial(port="COM4", baudrate=9600)

createGUI(ser)
ser.close()
