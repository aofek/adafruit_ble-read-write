#   1x3_dc_measurements_ble_to_pc

# boot section
import esp
import esp32
import micropython
from micropython import const
import machine
from machine import Pin,I2C,SoftI2C,ADC,Timer
import utime
import time
from time import sleep_ms
import struct
import random
import network
import ubluetooth
from ubluetooth import BLE
adcamp1=ADC(Pin(36))
adcamp2=ADC(Pin(39))
adcamp3=ADC(Pin(34))
adcbat=ADC(Pin(35))
led2=Pin(5,Pin.OUT)
srp=Pin(32,Pin.OUT)
srn=Pin(33,Pin.OUT)
machine.freq(240000000)

#------------------------------------------

class BLE():            # BLE class
    def __init__(self, name):   
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
                
        self.led=led2
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
                
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))
        sleep_ms(50)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))   

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
                    
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)            
            if message == 'led':
                led2.value(not led2.value())
                print('led2', led2.value())
                ble.send('led2' + str(led2.value()))
            if message=='hmc':
                magdat=adc_loop()
                ble.send(str(magdat))  
    
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        utime.sleep(0.001)
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)

#----------------------------------------
def adc_loop():
    amp1 =adcamp1.read()
    amp1=amp1+1000
    amp2 =adcamp2.read()
    amp2=amp2+1000
    amp3 =adcamp3.read()
    amp3=amp3+1000
    bat =adcbat.read()
    bat=bat+1000
    magdat=[amp1]+[amp2]+[amp3]+[bat]
    print(magdat)
    return magdat
#--------------------------------------------------------

if __name__ == '__main__':
    ble = BLE('hmc001')
   




