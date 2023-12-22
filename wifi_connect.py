import network
import socket
import time
import vars


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(vars.SSID, vars.PASSWORD)

    print("Connecting to WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print()

    print("Connected. Network config:", wlan.ifconfig())


def start_web_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Listening on", addr)

    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        request = cl.recv(1024)
        print("Request:", request)

        response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += "<html><body><h1>Hello World</h1></body></html>"

        cl.send(response)
        cl.close()


connect_to_wifi()
start_web_server()
