from RPLCD.i2c import CharLCD
from time import sleep

# Cambia '0x27' por la dirección I2C correcta de tu dispositivo
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

def main():
    
    lcd.clear()

    while True:
        try:
            lcd.cursor_pos = (0, 0)
            lcd.write_string("   AgrobotV2   ")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("      UAO      ")
            
        except KeyboardInterrupt:
            break

    lcd.clear()

if __name__ == "__main__":
    main()

