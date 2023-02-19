## General Info
- The IP address of the Raspberry Pi Pico W I have mounted on the car right now (using the breadboard): **10.0.0.214**

## Example Posts
Turns the "safeties" off (must do this first):
```
POST 10.0.0.214
{
    "mac": 0
}
```

Move forward for one second at 50% power:
```
POST 10.0.0.214
{
    "mac": 3,
    "power": 0.5,
    "duration": 1.0
}
```

If the `duration` parameter is **not specified**, it will continue what you told it to do until you make another call to it.

Go look at the *mac* settings in the [settings](./src/settings.py) to see what each MAC command does.


To get the status:
```
GET 10.0.0.214/status
```


## Distance Measurements
52 inches

|Surface|MAC|Power|Duration|Distance|
|-|-|-|-|-|
