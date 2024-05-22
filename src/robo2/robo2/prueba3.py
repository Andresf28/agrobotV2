from RPLCD.i2c import CharLCD
from time import sleep

# Cambia '0x27' por la dirección I2C correcta de tu dispositivo
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

def main():
    lcd.clear()
    lcd.write_string("Testing....")
    sleep(1)
    lcd.clear()

    for j in range(2):
        for i in range(16):
            lcd.cursor_pos = (j, i)
            lcd.write_string("*")
            sleep(0.1)
    lcd.clear()

    while True:
        try:
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Enter String you")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("want to display")
            sleep(1)
            lcd.clear()
            
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Sebastian la mas perra")
            sleep(2)
            lcd.clear()
        except KeyboardInterrupt:
            break

    lcd.clear()

if __name__ == "__main__":
    main()

