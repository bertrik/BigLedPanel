import serial
import time

class Ledboard:
    def __init__(self,port,speed):
        self.ser = serial.Serial(port, speed, timeout=1)
        self.framebuffer = bytearray([0x00] * 92)
        time.sleep(1)

    def writebuffer(self, data):
        if len(data) == 90:
            self.framebuffer = data
            self.draw()

    def width(self):
        return 15

    def drawpixels(self, b):
        self.framebuffer = bytearray([0x00] * 92)
        self.framebuffer[0] = 0x81
        self.framebuffer[1] = 0x80

        i = 2
        for bc in b:
            self.framebuffer[i] = bc & 127
            i += 1

        self.draw()

    def drawstring(self, string, font):
        self.framebuffer = bytearray([0x00] * 92)
        self.framebuffer[0] = 0x81
        self.framebuffer[1] = 0x80

        i = 2
        for char in string:
            c = ord(char) - 32
            self.framebuffer[i] = font[c][0]
            i += 1
            self.framebuffer[i] = font[c][1]
            i += 1
            self.framebuffer[i] = font[c][2]
            i += 1
            self.framebuffer[i] = font[c][3]
            i += 1 
            self.framebuffer[i] = font[c][4]
            i += 1 

            # beetje ruimte tussen de letters voor de meer leesbaar
            i += 1 

        self.draw() 
 
    def draw(self):
        self.ser.write(self.framebuffer)
        self.ser.reset_input_buffer()

    def demo(self):
        for i in range(0,89):
            self.framebuffer[i]=i

        while True:
            self.draw()
            time.sleep(0.01)
