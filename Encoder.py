from RPi import GPIO

class Encoder:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.encoder = (10, 9)
        GPIO.setup(self.encoder[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoder[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.encoder_last_A, self.encoder_last_B, self.encoder_value, self.encoder_range = None, None, None, None
##        self.encoder_last_A, self.encoder_last_B, self.encoder_value = GPIO.input(self.encoder[0]), GPIO.input(self.encoder[1]), 0
    
    def work_step(self):
        a_state = GPIO.input(self.encoder[0])
        b_state = GPIO.input(self.encoder[1])
        if self.encoder_last_A == 0 and self.encoder_last_B == 0:
            if a_state == 1 and b_state == 0:
                self.encoder_value += 1
            elif a_state == 0 and b_state == 1:
                self.encoder_value -= 1
        elif self.encoder_last_A == 0 and self.encoder_last_B == 1:
            if a_state == 0 and b_state == 0:
                self.encoder_value += 1
            elif a_state == 1 and b_state == 1:
                self.encoder_value -= 1
        elif self.encoder_last_A == 1 and self.encoder_last_B == 0:
            if a_state == 1 and b_state == 1:
                self.encoder_value += 1
            elif a_state == 0 and b_state == 0:
                self.encoder_value -= 1
        elif self.encoder_last_A == 1 and self.encoder_last_B == 1:
            if a_state == 0 and b_state == 1:
                self.encoder_value += 1
            elif a_state == 1 and b_state == 0:
                self.encoder_value -= 1
        self.encoder_last_A = a_state
        self.encoder_last_B = b_state


if __name__ == "__main__":
    enc = Encoder()
    while 1:
        enc.work_step()
        print(enc.encoder_value)
