import network
import socket
import time
from vars import SSID, PASSWORD
from machine import Pin

led = Pin(15, Pin.OUT)

ssid = SSID
password = PASSWORD

def url_decode(s):
    replacements = {'%20': ' ', '%21': '!', '%22': '"', '%23': '#', '%24': '$',
                    '%25': '%', '%26': '&', '%27': "'", '%28': '(', '%29': ')',
                    '%2A': '*', '%2B': '+', '%2C': ',', '%2D': '-', '%2E': '.',
                    '%2F': '/', '%3A': ':', '%3B': ';', '%3C': '<', '%3D': '=',
                    '%3E': '>', '%3F': '?', '%40': '@', '%5B': '[', '%5D': ']'}
    for encoded, decoded in replacements.items():
        s = s.replace(encoded, decoded)
    return s

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Initialize the text file
text_file_content = "This is a shared text file. Feel free to edit!"

# HTML template
html_template = """<!DOCTYPE html>
<html>
    <head> 
        <title>Pico Editor</title> 
        <script type="text/javascript">
            function fetchUpdates(){
                fetch('/fetch')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById("editor").value = data;
                        })
                    .catch((error) => console.error('Fetch error:', error));
                        }
            setInterval(fetchUpdates, 2000);  // Fetch updates every 2 seconds
        </script>
    </head>
    <body>
        <h1>Pico Collaborative Editor</h1>
        <form action="/" method="post">
            <textarea id="editor" name="text" rows="10" cols="30">{}</textarea><br>
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
        request = str(request, 'utf-8')

        if "POST" in request:
            # Locate and decode the text
            marker = "\r\n\r\n"
            post_data_start = request.find(marker) + len(marker)
            post_data = request[post_data_start:]
            new_text = url_decode(post_data[5:])
            text_file_content = new_text

        if "/fetch" in request:
            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n")
            cl.send(text_file_content)
        else:
            response = html_template.format(text_file_content)
            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            cl.send(response)

        cl.close()

    except OSError as e:
        cl.close()
        print("connection closed")
