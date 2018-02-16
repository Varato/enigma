#!/usr/bin/python3

"""
This python script simulates 3-rotor enigma machine.
"""
import sys

class enigma:
    def __init__(self):
        self.__wheel_read = [0,0,0]
        # describing the rotators position
        self.__accum = 0 #self.__wheel_read[0]*26*26 + self.__wheel_read[1]*26 + self.__wheel_read[2]
        self.__r = [[(self.__wheel_read[0] + i)%26 for i in range(26) ],
                    [(self.__wheel_read[1] + i)%26 for i in range(26) ],
                    [(self.__wheel_read[2] + i)%26 for i in range(26) ]]
        
        # the inner wiring of each rotators is a map, which will be never changed
        self.__rotors = ((3, 4, 13, 24, 7, 17, 8, 16, 10, 20, 1, 18, 14,
                            19, 5, 15, 23, 25, 6, 21, 12, 2, 9, 11, 22, 0),
                           (0, 16, 13, 6, 14, 21, 4, 5, 17, 12, 9, 11, 24,
                            22, 20, 1, 3, 23, 19, 2, 18, 15, 25, 8, 10, 7),
                           (25, 10, 17, 20, 14, 16, 9, 18, 13, 4, 1, 7, 5,
                            22, 3, 21, 11, 15, 23, 6, 19, 24, 2, 12, 0, 8))
        # feflector is pairs matching 0->24 24->0 ... never change
        self.__reflector = ((0,  1,  2,  3, 4,  5,  6,  8,  9,  10, 12, 19, 21),
                            (24, 17, 20, 7, 16, 18, 11, 15, 23, 13, 14, 25, 22))
    
    def __rot_map(self, pos_in):
        pos = pos_in
        for i in range(len(self.__rotors)):
            # retrieve the signal incomming pin, i.e. input pin of ith rotator
            pin_in = self.__r[i][pos]
            # get the output pin of rotator i
            pin_out = self.__rotors[i][pin_in]
            # get the absolute position of the output of ith rotator
            pos = self.__r[i].index(pin_out)            
        return pos
        
    def __inv_rot_map(self, pos_back):
        pos = pos_back
        for i in range(len(self.__rotors) - 1, -1, -1):
            pin_in_back = self.__r[i][pos]
            pin_out_back = self.__rotors[i].index(pin_in_back)
            pos = self.__r[i].index(pin_out_back)
        return pos
    
    def __reflect(self, pos):
        row = pos in self.__reflector[1]
        pal = self.__reflector[1-row][self.__reflector[row].index(pos)]
        return pal
    
    def __rot_wheel(self):
        self.__accum = (self.__accum + 1) % 26**3
        self.__wheel_read[2] = self.__accum % 26
        self.__wheel_read[1] = (self.__accum//26) % 26
        self.__wheel_read[0] = (self.__accum//26**2) % 26
        self.__r = [[(self.__wheel_read[0] + i)%26 for i in range(26)],
                    [(self.__wheel_read[1] + i)%26 for i in range(26)],
                    [(self.__wheel_read[2] + i)%26 for i in range(26)]]
        
    def __press(self, pos_in):
        self.__rot_wheel()
        output = self.__inv_rot_map(self.__reflect(self.__rot_map(pos_in)))
        return output

    def set_wheel(self, wheel_read):
        if isinstance(wheel_read, list) and len(wheel_read) == 3 and\
         0<=wheel_read[0]<=26 and 0<=wheel_read[1]<=26 and 0<=wheel_read[2]<=26:
            self.__wheel_read = wheel_read
            self.__accum = self.__wheel_read[0]*26*26 + self.__wheel_read[1]*26 + self.__wheel_read[2]
            self.__r = [[(self.__wheel_read[0] + i)%26 for i in range(26) ],
                        [(self.__wheel_read[1] + i)%26 for i in range(26) ],
                        [(self.__wheel_read[2] + i)%26 for i in range(26) ]]

    def press(self, char_in):
        if isinstance(char_in, str) and len(char_in) == 1:
            output = self.__press(ord(char_in) - 97)
            return output
        else:
            raise ValueError("input must be a single character")


    def transform(self, message, wheel_read):
        l = map(ord, message.strip().lower())
        msg = map( chr, filter(lambda x: 97<=x<=122, l) )
        self.set_wheel(wheel_read)
        
        cipher = ""
        for char in msg:
            cipher += chr(self.__press(ord(char) - 97) + 97)
        return cipher
   
if __name__ == "__main__":
    message = sys.argv[1]
    r0 = int(sys.argv[2])
    r1 = int(sys.argv[3])
    r2 = int(sys.argv[4])
    e = enigma()
    cipher = e.transform(message, [r0, r1, r2])
    print(cipher)
