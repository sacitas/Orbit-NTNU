import RPi.GPIO as GPIO
from RPLCD import i2c
import time
import pandas as pd
import FTTRv4_temp as tmp

#auto = 0

degree_sign = u'\N{DEGREE SIGN}'
 
 
 
def button_callback():
    if (GPIO.input(24) == 0 and ledState == 0):
        GPIO.output(15, True)
        ledState = 1
        time.sleep(0.5)
        auto_mode()  
    else:
        GPIO.output(15, False)
        ledState = 0
        time.sleep(0.5)
        man_mode()

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.add_event_detect(24, GPIO.RISING, callback=button_callback)

ledState = 0

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi


# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

framebuffer = [
    'Orbit NTNU',
    '',
]

def write_to_lcd(lcd, framebuffer, num_cols):
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')


def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.1):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s)- num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)

long_string = 'Like and subscribe or I will delete your Minecraft account'




def auto_mode():
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        SP = str(conf[0])
    temp0 = tmp.read_temp0()
    temp0 = str(temp0)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("SP: " + SP + " " + degree_sign + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
    time.sleep(0.5)

    
def man_mode():
    temp0 = tmp.read_temp0()
    temp0 = str(temp0)
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        man = str(conf[5])
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("ManVal: " + man)
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
    time.sleep(0.5)



try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(3)
    while True:
        with open ('pid.conf', 'r+') as g:
            conf = g.readline().split(',')
            auto = int(conf[4])
        button_callback() 

            
except KeyboardInterrupt:
    lcd.clear()
    loop_string(long_string, lcd, framebuffer, 1, 16)
#   lcd.write_string("Goodbye")
    time.sleep(2)
    lcd.close(clear = True)
    GPIO.cleanup()
