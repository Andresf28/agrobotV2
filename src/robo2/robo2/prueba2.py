import smbus
import time

# Dirección del dispositivo I2C (puedes usar i2cdetect para encontrarla)
LCD_ADDRESS = 0x27

# Comandos para el LCD
LCD_CMD = 0x0
LCD_CHR = 0x40

# Control de líneas
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# Control de caracteres por línea
LCD_WIDTH = 16

# Modos de control de la pantalla
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

# Inicialización
LCD_FUNCTIONSET = 0x20 | 0x00 | 0x04
LCD_DISPLAYCONTROL = 0x08 | 0x04
LCD_CLEARDISPLAY = 0x01
LCD_ENTRYMODESET = 0x04 | 0x02

bus = smbus.SMBus(1)  # Selecciona el bus I2C

def lcd_init():
    # Inicialización del LCD
    lcd_byte(0x03)
    lcd_byte(0x03)
    lcd_byte(0x03)
    lcd_byte(0x02)

    lcd_byte(LCD_FUNCTIONSET | 0x08 | 0x04)  
    lcd_byte(LCD_DISPLAYCONTROL | 0x04)
    lcd_byte(LCD_CLEARDISPLAY)
    lcd_byte(LCD_ENTRYMODESET | 0x02)
    time.sleep(0.2)

def lcd_byte(bits, mode=LCD_CMD):
    # Envía un byte al LCD
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(LCD_ADDRESS, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(LCD_ADDRESS, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Activa el pin de habilitación del LCD
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits & ~0x04))
    time.sleep(0.0005)

def lcd_string(message, line):
    # Envia una cadena al LCD
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

if __name__ == "__main__":
    try:
        lcd_init()
        while True:
            lcd_string("Hola, Mundo!", LCD_LINE_1)
            lcd_string("Desde Jetson TX2", LCD_LINE_2)
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(LCD_CLEARDISPLAY)

