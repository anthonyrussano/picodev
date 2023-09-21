import network
import socket
import time
import ure
from vars import SSID, PASSWORD  # Make sure to provide these variables in a file named vars.py
from machine import Pin

led = Pin(15, Pin.OUT)

ssid = SSID
password = PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

messages = []

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> 
        <h1>Pico W</h1>
        <form action="/" method="post">
            <input type="text" name="message" placeholder="Type your message">
            <input type="submit" value="Send">
        </form>
        <ul>
            %s
        </ul>
    </body>
</html>
"""

# Wait for network connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print("ip = " + status[0])

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print("listening on", addr)

while True:
    try:
        cl, addr = s.accept()
        print("client connected from", addr)
        request = cl.recv(1024)
        request = str(request)

        # Extract message from POST data
        match = ure.search("message=(.+?) ", request)
        if match:
            message = match.group(1).replace('+', ' ')
            messages.append(message)

        # Create response
        message_list = "".join(["<li>{}</li>".format(m) for m in messages])
        response = html % message_list

        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print("connection closed")
