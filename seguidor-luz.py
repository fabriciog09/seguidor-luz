#!/usr/bin/python

import time

import sys

#Importamos la libreria PyBot 
sys.path.insert(0, '/home/olpc/Activities/TurtleBots.activity/plugins/butia')

sys.path.insert(0, "/usr/share/sugar/activities/TurtleBots.activity/plugins/butia")

# Importamos el modulo de pybot
from pybot import usb4butia

# Generamos una instancia de la placa USB4Butia
robot = usb4butia.USB4Butia()
robot.refresh()


# Definimos una comprador de dos numeros aplicando un tolerancia
tolerance = 5000
def isBigger(num1, num2, tolerance):
    return (num1 - tolerance)>num2


# Para eliminar las diferencias en las mediciones de los sensores provocadas por la luz ambiente almacenamos
# el valor inicial y para eliminar errores de medicion de los sensores utilizamos el promedio de 10 mediciones

acumulateTopLight = 0
for i in range(10):
    acumulateTopLight += robot.getLight(1) 
topLight_init = acumulateTopLight / 10

acumulateBottomLight = 0
for i in range(10):
    acumulateBottomLight += robot.getLight(3)
bottomLight_init =  acumulateBottomLight / 10

acumulateLeftLight = 0
for i in range(10):
    acumulateLeftLight += robot.getLight(5)
leftLight_init = acumulateLeftLight / 10

acumulateRightLight = 0
for i in range(10):
    acumulateRightLight += robot.getLight(6)
rightLight_init = acumulateRightLight /10


# Para evitar errores en los sensores cada vez que tomamos un promedio de 10 mediciones
# y luego le restamos el valor inicial 

def getTopLight():
    acumulateTopLight = 0
    for i in range(10):
        acumulateTopLight += robot.getLight(1) 
    return (acumulateTopLight/10) - topLight_init

def getBottomLight():
    acumulateBottomLight = 0
    for i in range(10):
        acumulateBottomLight += robot.getLight(3)
    return (acumulateBottomLight/10) - bottomLight_init


def getLeftLight():
    acumulateLeftLight = 0
    for i in range(10):
        acumulateLeftLight += robot.getLight(5)
    return (acumulateLeftLight/10) - leftLight_init


def getRightLight():
    acumulateRightLight = 0
    for i in range(10):
        acumulateRightLight += robot.getLight(6)
    return (acumulateRightLight/10) - rightLight_init



# Definimos las funciones para el desplazamiento de los motores.
def goRight():
    robot.set2MotorSpeed(1, 200, 0, 0)
    print("goRight")

def goLeft():
    robot.set2MotorSpeed(0, 200, 0, 0)
    print("goLeft")

# Debido a que el movimiento hacia arriba exige mayor esfuerzo 
# del motor aumentamos el valor de la velocidad de este
def goUp():
    robot.set2MotorSpeed(0, 0, 0, 500)
    print("goUp")

def goDown():
    robot.set2MotorSpeed(0, 0, 1, 100)
    print("goDown")

def stop():
    robot.set2MotorSpeed(0, 0, 0, 0)
    print("stop")

# En cada interaccion comparamos las mediciones de los sensores y desplazamos los motores segun corresponda
# Primero se realiza el movimiento vertical y cuando la ubicacion vertical es las deseada se realiza el 
# desplazamiento horizontal
while (True):
    topLight = getTopLight()
    print( "Top Light",topLight)
    bottomLight = getBottomLight()
    print( "Botom Light", bottomLight)
    # Si el valor del sensor superior es mayor al inferior se realiza un movimiento hacia arriba
    if isBigger(topLight,bottomLight, tolerance * 2) : 
        goUp()
    # Si el valor del sensor inferior es mayor al superior se realiza un movimiento hacia abajo
    elif isBigger(bottomLight,topLight, 0) : 
        goDown()
    else:
        leftLight = getLeftLight()
        print( "Left Light",leftLight)
        rightLight = getRightLight()
        print( "Right Light", rightLight)
        # Si el valor del sensor izquierdo es mayor al derecho se realiza un movimiento hacia la izquierda
        if isBigger(leftLight,rightLight, tolerance) : 
            goLeft()
        # Si el valor del sensor derecho es mayor al izquierdo se realiza un movimiento hacia la derecha
        elif isBigger(rightLight,leftLight, tolerance) : 
            goRight()
    # Cada movimiento se realiza con un segundo de duracion
    time.sleep(1)
    stop()
    time.sleep(1)
