#librerías, I2C, Y LCD
import utime
import machine
import uos
from machine import Pin, I2C, UART
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from max6675 import MAX6675
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

#DECLARACION MAX
so = Pin(15, Pin.IN)
sck = Pin(13, Pin.OUT)
cs = Pin(14, Pin.OUT)
 
max = MAX6675(sck, cs , so)



uart = UART(1, 9600)
# Función para enviar datos a LabVIEW


def test_main():
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
    lcd.putstr("Toma de temperatura")
    utime.sleep(2)
    lcd.clear()
    count = 0
    
    while True:
        #DEFINICIONES DE LA TEMPERATURAS:
        temp = max.read()
        rankine = temp *1.8 + 491.67
        kelvin = temp + 273.15
        fahrenheit = (temp * 9/5) + 32
        #Voltaje  (5 volt es el voltaje maximo y 1024 la temperatura maxima segun el datasheet, temp es el dato retornado por el sensor)
        voltaje = (5/1024)*temp
        #VoltajeMicros relacion de la tabla
        Vu = 0.0406*temp+0.0119
        #RANKIN
        lcd.move_to(0, 0)
        lcd.putstr("R:" + "{:.1f}".format(rankine))
        #CELSIUS
        lcd.move_to(0, 1)      
        lcd.putstr("C:" + "{:.1f}".format(temp))
        #VOLTAJE
        lcd.move_to(13, 1)
        lcd.putstr("uV:" + "{:.2f}".format(Vu))
        #KELVIN
        lcd.move_to(0, 2)
        lcd.putstr("K:" + "{:.1f}".format(kelvin)) 
        #FARENHEIT
        lcd.move_to(0, 3)
        lcd.putstr("F:" + "{:.1f}".format(fahrenheit))
        temp = str(temp)
        uart.write(temp+"\n")
        
        #Apagado de pantalla
        data= uart.readline()
        if data is not None:
            data = decode().strip()
            if data == "x":
                lcd.backlight_off()
            elif data == "y":
                lcd.backlight_on()
#while True
test_main()









