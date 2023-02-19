# Wifi
ssid = ""
password = ""


# GPIO Pins. GP #'s, not pin numbers

# HC-SR04 ultrasonig range finder module
gpio_hcsr04_trigger = 17
gpio_hcsr04_echo = 16

#rear right
gpio_rr_safety = 0
gpio_rr_forward = 2
gpio_rr_backward = 1

#rear left
gpio_rl_safety = 3
gpio_rl_forward = 4
gpio_rl_backward = 13

#front right
gpio_fr_safety = 9
gpio_fr_forward = 15
gpio_fr_backward = 14

#front left
gpio_fl_safety = 6
gpio_fl_forward = 7
gpio_fl_backward = 8

# Movement Action Code, or MAC's:
mac_safety_off_all = 0
mac_safety_on_all = 1
mac_idle = 2
mac_forward = 3
mac_turn = 4
mac_sideway = 5