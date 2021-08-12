
import time
from adafruit_ble import BLERadio,BLEConnection
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.services import Service
from adafruit_ble.services.nordic import UARTService
import keyboard
import mouse

#-----------------------------

bler = BLERadio()
blec = BLEConnection
ches = Characteristic()
srvs = Service
conn=0

#---------------------------------------

def ble_search(search,conn):
    for advertisement in bler.start_scan():
        if conn==0:
            address = advertisement.address
            name=advertisement.complete_name
            if name.find('hmc') == 0:
                print(name,address.string)
                if (advertisement.connectable):
                    connection = bler.connect(advertisement,timeout=10)
                    if connection.connected:
                        conn=1
                        print("conn =",conn)
                        return name,address,conn,srvs,connection
                    
#---------------------------------------

def s_r_show(go_on): 
    avc=0
    disp=2000 
    ave=2400
    while True:
                
        uart.write(b"hmc")
        time.sleep(0.1)
        dat = uart.read(25)# 25 fixed number for 4 datas 
        magz=int(dat[12:17])-1000
        disp=int((disp*2+magz)/3)
        p=(disp-(ave-10))*20+200
        
        mouse.move(p,p)
      
#------------------------
        avc=avc+1
        if avc<=50:
            ave=(ave+magz)/2
            if avc==5:
                print('biasing')
        elif avc==55:
            batadc=(int(dat[19:23])-1000)/950
            bat=round(batadc,2)
            print('battery voltage= ',bat)
            print('measure')
#----------------------
        if keyboard.is_pressed('q'):
            print('disconnect')
            break
#-----------------------           

def ble_disconnect(disc):
    time.sleep(1)
    if bler.connected:
        for c in bler.connections[0:1]:
            c.disconnect()
            print ('disconnected')
            break
    
#-------------------------------------------
if __name__=='__main__':
    name,address,conn,srvs,connection = ble_search(True,conn)
    
    uart = connection[UARTService]
    s_r_show(go_on=1)
     
    disc=True
    ble_disconnect(disc)
    
    
    
    
    