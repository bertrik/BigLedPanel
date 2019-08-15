import serial
import time

class Ledboard:
    def __init__(self,port,speed):
        self.ser = serial.Serial(port, speed, timeout=1)
        self.framebuffer = [0x00] * 90
        time.sleep(1)

    def writebuffer(self, data):
        if len(data) == 90:
            self.framebuffer = data
            self.draw()

    def drawstring(self, string, font):
        i = 0
        self.framebuffer = [0x00] * 90
        for char in string:
            self.framebuffer[i] = font[ord(char)-32][0]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][1]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][2]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][3]
            i += 1 
            self.framebuffer[i] = font[ord(char)-32][4]
            i += 1 
        self.draw() 
 
    def draw(self):
        self.ser.write(chr(0x81))
        self.ser.write(chr(0x80))

        for frame in self.framebuffer:
        #    while self.ser.out_waiting > 0:
        #        print self.ser.out_waiting
                #time.sleep(.30)

            self.ser.write(chr(frame))

        #time.sleep(.20)

        self.ser.reset_input_buffer()
            
        self.ser.flush()

    def demo(self):
        for i in range(0,89):
            self.framebuffer[i]=i

        while True:
            self.draw()
            time.sleep(0.01)
