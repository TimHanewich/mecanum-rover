import mp_wlan
import socket
import json
import toolkit
import driver
import settings
import time
import requests_tools
import HCSR04
import voltage_sensor
import LiPo
import machine

# first, blink the LED twice
# please note that this is the way to do it for the Raspberry Pi Pico W... providing 'LED' as  the pin number.
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
time.sleep(0.5)
led.off()
time.sleep(0.5)
led.on()
time.sleep(0.5)
led.off()
time.sleep(0.5)

# turn the LED on and leave it like tht
led.on()


# variables to track
stat_request_count = 0
stat_instruction_count = 0
stat_online_at_ticks = time.ticks_ms()

# create the voltage sensor module and LiPo battery status
vs = voltage_sensor.voltage_sensor(28)
battery = LiPo.LiPo()

# create the HC-SR04 module
ultrasonic = HCSR04.HCSR04(settings.gpio_hcsr04_trigger, settings.gpio_hcsr04_echo)

# create the driver
d = driver.mecanum_driver()
d.setup()

# connect
my_ip = mp_wlan.try_connect()
print("Online! My IP is '" + str(my_ip) + "'")

# set up
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Now listening on '" + str(addr) + "'!")

while True:
    cl, addr = s.accept()
    print("Client connected from " + str(addr))
    request = cl.recv(1024)
    print("Request: " + str(request))

    # parse into a request
    stat_request_count = stat_request_count + 1 #increment request count
    request_str = request.decode()
    r = requests_tools.request.parse(request_str)

    if r.path == "/" and r.method.upper() == "POST":

        # was a body included
        body:str = None
        if r.body != "":
            body = r.body
        else:

            # find the header that states the length
            body_length:int = None
            for key, value in r.headers.items():
                if key.lower() == "content-length":
                    body_length = int(value)

            if body_length != None:
                bodyb = cl.recv(body_length)
                body = bodyb.decode()

        # Get the body as JSON
        payload = json.loads(body)

        # Assemble a list of instructions to execute
        to_execute = []
        if type(payload) == dict:
            to_execute.append(payload) #add this single object to the list of things to do
        elif type(payload) == list:
            for obj in payload:
                to_execute.append(obj)


        # go through and execute each
        for instruction in to_execute:

            # increment stat
            stat_instruction_count = stat_instruction_count + 1

            # set variables
            mac = None
            power = None
            duration = None

            # get variables
            try:
                mac = instruction["mac"]
            except:
                mac = None
            try:
                power = instruction["power"]
            except:
                power = None
            try:
                duration = instruction["duration"]
            except:
                duration = None

            # act on the mac
            if mac == settings.mac_safety_off_all:
                print("Safety off all")
                d.safety_off_all()
            elif mac == settings.mac_safety_on_all:
                print("Safety on all")
                d.safety_on_all()
            elif mac == settings.mac_idle:
                print("idle")
                d.idle()
            elif mac == settings.mac_forward:
                print("forward")
                if power != None:
                    d.forward(power)
            elif mac == settings.mac_turn:
                print("turn")
                if power != None:
                    d.turn(power)
            elif mac == settings.mac_sideway:
                print("side")
                if power != None:
                    d.sideway(power)

            # if there was a duration, wait (duration is in seconds)
            if duration != None:
                time.sleep_ms(round(float(duration)*1000))
                d.idle() # then go to idle after doing it for that long


        # Return success response
        cl.send("HTTP/1.0 200 OK\r\n\r\n")
        cl.close()

    elif r.path.lower() == "/status":

        ToReturn = {}
        
        # number of requests
        ToReturn["requests"] = stat_request_count

        # number of instructions
        ToReturn["instructions"] = stat_instruction_count

        # online for (seconds)
        elapsed_ticks = time.ticks_ms() - stat_online_at_ticks
        elapsed_seconds = elapsed_ticks / 1000
        ToReturn["age"] = elapsed_seconds

        # distance
        # distance_cm = ultrasonic.measure()
        # ToReturn["distance"] = distance_cm

        # battery level
        volts = vs.measure_set()
        battery_percent = battery.percentage(volts)
        ToReturn["battery"] = battery_percent

        # Return success response
        cl.send("HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n" + str(json.dumps(ToReturn)))
        cl.close()
