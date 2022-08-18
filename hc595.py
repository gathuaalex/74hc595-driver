from machine import Pin

class Hc595:
    """
    serial_in_pin   ->    SER (data) on 74hc595 to send 1s and 0s to the shift register.

    latch_pin       ->    RCLK (register clock or latch pin) on 74hc595 to tell the shift register to
                            output the mixture of high and low voltages we have previously sent.

    clock_pin       ->    SRCLK (clock pin) on 74hc595 to tell the shift register to accept an input.

    """
    def __init__(self, serial_in_pin: int= 12, latch_pin: int= 14, clock_pin: int= 27 ):
        """
        constructor for the Hc595 class
        """
        # 74hc595 pin configuration
        self.data=Pin(serial_in_pin,Pin.OUT,value=0)
        self.latch=Pin(latch_pin,Pin.OUT,value=0)
        self.clock=Pin(clock_pin,Pin.OUT,value=0)

        # defining outbits and reset_bits
        #[msb,*,*,*,*,*,*lsb] -> pins [0,1,2,3,4,5,6,7]
        self.out_bits=[0,0,0,0,0,0,0,0]
        self.reset_bits=self.out_bits.copy()


    def shiftout(self, pin: int, toggle: bool= False, master_reset: bool= False):
        # stores the list of bits to store
        # that is reset and data bits
        exec_bits=[] 
        # checks if command is to reset the shift register 
        if master_reset:
            exec_bits.extend(self.reset_bits)

        else:
            assert pin in range(0,8), "Pin number must be between 0 and 7"
            
            self.out_bits[pin] = 0 if toggle else 1 # set the pin to high or low depending on the toggle value

            exec_bits.extend(self.out_bits)


        #shift out the data starting with the most significant bit(MSB)
        for bit in exec_bits:
            self.data.value(bit)
            #shift the data to the shift register
            self.clock.value(1)#set the clock pin to high
            self.clock.value(0)

        #latch the data to the output pins
        # data is present at the output pins
        self.latch.value(1)
        self.latch.value(0)

        return self.out_bits
