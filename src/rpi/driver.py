import machine
import settings
import toolkit

class mecanum_driver:

    # Safety (0 or 1) objects
    rr_safety = None
    rl_safety = None
    fr_safety = None
    fl_safety = None

    # PWM objects
    rr_forward = None
    rr_backward = None
    rl_forward = None
    rl_backward = None
    fr_forward = None
    fr_backward = None
    fl_forward = None
    fl_backward = None

    # codes
    fl = 0
    fr = 1
    rl = 2
    rr = 3

    def setup(self):
        
        # set up safeties
        self.rr_safety = machine.Pin(settings.gpio_rr_safety, machine.Pin.OUT)
        self.rl_safety = machine.Pin(settings.gpio_rl_safety, machine.Pin.OUT)
        self.fr_safety = machine.Pin(settings.gpio_fr_safety, machine.Pin.OUT)
        self.fl_safety = machine.Pin(settings.gpio_fl_safety, machine.Pin.OUT)

        # set up PWM's
        self.rr_forward = machine.PWM(machine.Pin(settings.gpio_rr_forward, machine.Pin.OUT))
        self.rr_backward = machine.PWM(machine.Pin(settings.gpio_rr_backward, machine.Pin.OUT))
        self.rl_forward = machine.PWM(machine.Pin(settings.gpio_rl_forward, machine.Pin.OUT))
        self.rl_backward = machine.PWM(machine.Pin(settings.gpio_rl_backward, machine.Pin.OUT))
        self.fr_forward = machine.PWM(machine.Pin(settings.gpio_fr_forward, machine.Pin.OUT))
        self.fr_backward = machine.PWM(machine.Pin(settings.gpio_fr_backward, machine.Pin.OUT))
        self.fl_forward = machine.PWM(machine.Pin(settings.gpio_fl_forward, machine.Pin.OUT))
        self.fl_backward = machine.PWM(machine.Pin(settings.gpio_fl_backward, machine.Pin.OUT))

        # set up PWM frequency
        self.rr_forward.freq(1000)
        self.rr_backward.freq(1000)
        self.rl_forward.freq(1000)
        self.rl_backward.freq(1000)
        self.fr_forward.freq(1000)
        self.fr_backward.freq(1000)
        self.fl_forward.freq(1000)
        self.fl_backward.freq(1000)

    def safety_off(self, wheel_code:int):
        if wheel_code == self.fl:
            self.fl_safety.high()
        elif wheel_code == self.fr:
            self.fr_safety.high()
        elif wheel_code == self.rl:
            self.rl_safety.high()
        elif wheel_code == self.rr:
            self.rr_safety.high()
        
    def safety_on(self, wheel_code:int):
        if wheel_code == self.fl:
            self.fl_safety.low()
        elif wheel_code == self.fr:
            self.fr_safety.low()
        elif wheel_code == self.rl:
            self.rl_safety.low()
        elif wheel_code == self.rr:
            self.rr_safety.low()

    def safety_off_all(self):
        self.safety_off(self.fl)
        self.safety_off(self.fr)
        self.safety_off(self.rl)
        self.safety_off(self.rr)

    def safety_on_all(self):
        self.safety_on(self.fl)
        self.safety_on(self.fr)
        self.safety_on(self.rl)
        self.safety_on(self.rr)
        
    def set_power(self, wheel_code:int, power:float):

        # get PWM's to affect
        pwm_forward = None
        pwm_backward = None
        if wheel_code == self.fl:
            pwm_forward = self.fl_forward
            pwm_backward = self.fl_backward
        elif wheel_code == self.fr:
            pwm_forward = self.fr_forward
            pwm_backward = self.fr_backward
        elif wheel_code == self.rl:
            pwm_forward = self.rl_forward
            pwm_backward = self.rl_backward
        elif wheel_code == self.rr:
            pwm_forward = self.rr_forward
            pwm_backward = self.rr_backward
        
        # set power
        if power == 0:
            pwm_forward.duty_u16(0)
            pwm_backward.duty_u16(0)
        elif power > 0:
            pwm_backward.duty_u16(0)
            pwm_forward.duty_u16(toolkit.percent_to_u16(power))
        elif power < 0:
            pwm_forward.duty_u16(0)
            pwm_backward.duty_u16(toolkit.percent_to_u16(power * -1))

    ########### MOVEMENT DIRECTIONS BELOW! ##############

    def idle(self):
        self.set_power(self.fl, 0)
        self.set_power(self.fr, 0)
        self.set_power(self.rl, 0)
        self.set_power(self.rr, 0)

    # positive power goes forward. Negative goes backward
    def forward(self, power:float):
        self.set_power(self.fl, power)
        self.set_power(self.fr, power)
        self.set_power(self.rl, power)
        self.set_power(self.rr, power)
    
    # positive power turns right, negative turns left
    def turn(self, power:float):
        self.set_power(self.fr, power * -1)
        self.set_power(self.rr, power * -1)
        self.set_power(self.fl, power)
        self.set_power(self.rl, power)

    # positive goes to right, negative goes towards left
    def sideway(self, power:float):
        self.set_power(self.fl, power)
        self.set_power(self.fr, power * -1)
        self.set_power(self.rl, power * -1)
        self.set_power(self.rr, power)
