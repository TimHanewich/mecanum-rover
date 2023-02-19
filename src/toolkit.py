import json
import math
import urequests

def json_body_from_request(request:bytes):
    parts = request.split(b"\r\n\r\n")
    body = parts[len(parts)-1]
    body = body.decode()
    obj = json.loads(body)
    return obj

def percent_to_u16(percent:float):
    tr = percent * 65025
    tri = math.floor(tr)
    return tri

def post(url:str, msg:str) -> None:
    print("Posting '" + msg + "' to '" + url + "'")
    x = urequests.post(url, data = msg)
    x.close()
