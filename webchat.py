import network
import socket
import time
from vars import SSID, PASSWORD
from machine import Pin

led = Pin(15, Pin.OUT)

ssid = SSID
password = PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Initialize the text file
text_file_content = "This is a shared text file. Feel free to edit!"

# HTML template
html_template = """<!DOCTYPE html>
<html>
    <head> <title>Pico Editor</title> </head>
    <body>
        <h1>Pico Collaborative Editor</h1>
        <form action="/" method="post">
            <textarea name="text" rows="10" cols="30">{}</textarea><br>
            <input type="submit" value="Update">
        </form>
    </body>
</html>
"""

# Wait for WLAN connection
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

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print("client connected from", addr)
        request = cl.recv(1024)
        request = str(request)

        if "POST" in request:
            start_idx = request.find("text=") + 5
            end_idx = request.find(" HTTP/1.1")
            new_text = request[start_idx:end_idx]
            new_text = new_text.replace("+", " ")
            text_file_content = new_text

        response = html_template.format(text_file_content)
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print("connection closed")
