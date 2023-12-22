import network
import time
import socket


def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body><h1>Hello World</h1></body></html>
         """
    return html


def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    ap.ifconfig(("192.168.4.3", "255.255.255.0", "192.168.4.3", "8.8.8.8"))

    while ap.active() == False:
        pass
    print("AP Mode Is Active, You can Now Connect")
    print("IP Address To Connect to:: " + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket object
    s.bind(("", 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        response = web_page()
        conn.send(response)
        conn.close()


ap_mode("NAME", "PASSWORD")
