import network
import socket
import time
from machine import Pin
from vars import SSID, PASSWORD

ssid = SSID
password = PASSWORD
LED_PIN = 15

def initialize_led(pin_number):
    return Pin(pin_number, Pin.OUT)

def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    return wlan

def check_wifi_status(wlan, max_wait=10):
    while max_wait > 0:
        status = wlan.status()
        if status == network.STAT_GOT_IP:
            print("WiFi connected")
            return True
        elif status in [network.STAT_WRONG_PASSWORD, network.STAT_NO_AP_FOUND]:
            print("Failed to connect to WiFi")
            return False

        print(f"Waiting for connection... {max_wait} attempts left")
        time.sleep(1)
        max_wait -= 1
    
    print("WiFi connection timed out")
    return False

def create_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print(f"Listening on {addr}")
    return s

def handle_client(cl, addr):
    print(f"Client connected from {addr}")
    request = cl.recv(1024)
    print(f"Received request: {request}")

    response = "Hello, world!"
    http_response = f"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n{response}"
    cl.send(http_response.encode())
    cl.close()

# Main Program
# Main Program
if __name__ == '__main__':
    led = initialize_led(LED_PIN)
    wlan = initialize_wifi(SSID, PASSWORD)

    if not check_wifi_status(wlan):
        raise RuntimeError("Network connection failed")

    print(f"IP address: {wlan.ifconfig()[0]}")

    server_socket = create_server()

    led_toggle_time = time.time()  # Initialize time counter for LED toggle
    led_state = False  # LED initial state

    while True:
        try:
            # Toggle LED every 30 seconds
            if time.time() - led_toggle_time >= 30:
                led_state = not led_state  # Invert LED state
                led.value(led_state)
                led_toggle_time = time.time()  # Reset time counter

            # Check for incoming client connections
            client_socket, client_addr = server_socket.accept()
            handle_client(client_socket, client_addr)
        except OSError as e:
            print(f"Connection closed: {e}")
