#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time

class Aspersion(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("aspersor") # MODIFY NAME
        self.get_logger().info("INICIANDO ASPERSIÓN")

        self.bombaPin = 12
        self.valvula1Pin = 23
        self.valvula2Pin = 24

        GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
        # set pin as an output pin with optional initial state of HIGH



        GPIO.setup(self.bombaPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.valvula1Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.valvula2Pin, GPIO.OUT, initial=GPIO.LOW)
        self.curr_value = GPIO.HIGH
        self.aspersion_continua()
    
    def aspersion_continua(self):
        

        while True:      
            time.sleep(0.0001)
            # Toggle the output every second a
            GPIO.output(self.bombaPin, self.curr_value)
            GPIO.output(self.valvula1Pin, self.curr_value)
            GPIO.output(self.valvula2Pin, self.curr_value)
            self.curr_value ^= GPIO.HIGH
        



def main(args=None):
    rclpy.init(args=args)
    node = Aspersion() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
