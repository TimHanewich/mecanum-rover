import driver
import HCSR04
import settings
import time
import pattern_recognition
import mp_wlan
import toolkit

def update_status(status:str) -> None:
    #murl = "https://webhook.site/83f709aa-0e31-4d13-bfc6-92fde2917ed0"
    #toolkit.post(murl, status)
    print("Status update: " + status)

# connect to wifi
#ip = mp_wlan.try_connect()
#update_status("Online! My IP: " + str(ip))

# post I'm online
#update_status("I'm online! My IP: " + str(ip))

# set up driver
d = driver.mecanum_driver()
d.setup()
d.safety_off_all()

# set up range finder
ultrasonic = HCSR04.HCSR04(settings.gpio_hcsr04_trigger, settings.gpio_hcsr04_echo)

# Find a point cloud
update_status("Starting loop now.")
data = []
cycle = None
while cycle == None:

    # measure + add
    m = ultrasonic.measure()
    data.append(m)
    update_status("Measurement taken: " + str(m))

    cycle = pattern_recognition.select_first_cycle(data)
    update_status("Cycle: " + str(cycle))

    # if cycle is still None, move on
    if cycle == None:
        update_status("Turning now.")
        d.turn(0.65)
        time.sleep(0.20)
        d.idle()

        # wait a sec
        time.sleep(0.5)


# WE FOUND IT!
update_status(str(cycle))

# Write it
update_status("Writing to memory...")
f = open("output.txt", "w")
f.write(str(cycle))
f.close()
update_status("Write complete!")
