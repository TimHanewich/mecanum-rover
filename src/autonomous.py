import driver
import HCSR04
import settings
import time

# set up driver
d = driver.mecanum_driver()
d.setup()
d.safety_off_all()

# set up ultrasonic range finder
ultrasonic = HCSR04.HCSR04(settings.gpio_hcsr04_trigger, settings.gpio_hcsr04_echo)

while True:
    
    # measure distance
    print("Measuring distance...")
    distance_cm = ultrasonic.measure()
    print("Distance: " + str(distance_cm) + " cm")

    # act on distance
    if distance_cm < 15:
        print("Turning...")
        d.turn(-0.65)
        time.sleep(0.8)
        d.idle()
    else: # distance is greater than 15
        
        # duration and power to move forward
        duration = None
        power = None

        # determine how far we should move forward
        if distance_cm < 25:
            duration = 0.35
            power = 0.50
        elif distance_cm < 35:
            duration = 0.5
            power = 0.55
        elif distance_cm < 50:
            duration = 0.8
            power = 0.65
        else:
            duration = 1
            power = 0.75



        # move a little bit
        print("Moving forward")
        d.forward(power)
        time.sleep(duration)
        d.idle()

        
    # wait a moment
    print("Sleeping...")
    time.sleep(2)
