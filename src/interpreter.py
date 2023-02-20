### SETTINGS ###
redirect_to:str = "10.0.0.214"
################


import socket
import json
import requests


class request:

    method:str = None
    path:str = None
    body:str = None
    headers:dict = {}

    @staticmethod
    def parse(full_request:str):
        ToReturn = request()
        
        # split
        parts = full_request.split("\r\n")

        # get the method
        p1 = parts[0]
        loc1 = p1.index(" ")
        tr = p1[0:loc1]
        ToReturn.method = tr

        # path
        p1 = parts[0]
        loc1 = p1.index(" ")
        loc2 = p1.index(" ", loc1 + 1)
        tr = p1[loc1+1:loc2]
        ToReturn.path = tr

        # body
        bs = full_request.split("\r\n\r\n")
        ToReturn.body = bs[1]

        # headers dictionary
        #get part before body
        before_body = bs[0]
        bb_parts = before_body.split("\r\n")
        for x in range(1, len(bb_parts)):
            this_header = bb_parts[x]
            cl = this_header.index(":")
            k = this_header[0:cl]
            v = this_header[cl+1:9999].strip()
            ToReturn.headers[k] = v

        return ToReturn
    


# print my IP address
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("My local IP address: '" + ip_address + "'")
print("I will redirect all network traffic to '" + redirect_to + "'")

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
s.bind(("", 80))

# Listen for incoming connections
s.listen(1)

print("Listening for incoming connections...")

while True:
    # Establish connection with client
    client, addr = s.accept()
    print("Connection from: " + str(addr))
    
    # read
    r = client.recv(9999)
    req:request = request.parse(r.decode())



    # handle a get and post differently
    if req.method.upper() == "POST":

        jobj = json.loads(req.body)

        # redirect
        url = "http://" + redirect_to + req.path
        headers = {"Content-Type": "application/json"}
        print("Sending...")
        response = requests.post(url, headers=headers, json=jobj)
        print("Complete!")
        
        # Respond with what we heard back
        client.send(("HTTP/1.0 " + str(response.status_code) + "\r\nContent-Type: application/json\r\n\r\n" + response.content.decode()).encode())
        client.close()

    elif req.method.upper() == "GET":
        
        # redirect
        url = "http://" + redirect_to + req.path
        print("Sending...")
        response = requests.get(url)
        print("Complete!")

        # Respond with what we heard back
        client.send(("HTTP/1.0 " + str(response.status_code) + "\r\nContent-Type: application/json\r\n\r\n" + response.content.decode()).encode())
        client.close()