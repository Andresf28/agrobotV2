import LiquidCrystal_I2C  
from time import sleep  
lcd=LiquidCrystal_I2C.lcd()  
lcd.clear()  
lcd.display("Testing....",1,0)  
sleep(1)
lcd.clear()
for j in range(1,3):
     for i in range(16):
         lcd.display("*",j,i)
         sleep(0.1)
lcd.clear()   
while True:  
   try: 
     lcd.display("Enter String you",1,0)
     lcd.display("want to display",2,0) 
     sleep(1)
     lcd.display("Sebastian gey",1,0)
     sleep(2)
     lcd.clear()    
   except KeyboardInterrupt:    
     break  
