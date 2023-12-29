## Basic Setup Instructions for running MicroPython on the ESP32-C3

- Download the most recent firmware:
  - https://micropython.org/download/ESP32_GENERIC_C3/
  - Example: `ESP32_GENERIC_C3-20231227-v1.22.0.bin`
- Checkout the esptool repository:
  - Repo URL: https://github.com/espressif/esptool
- Install esptool python package
  - `pipenv install esptool`
- Connect the esp32c3 chip to your computer.
- Run esptool.py commands:
  - `pipenv run python esptool.py --chip esp32c3 --port /dev/ttyACM0 erase_flash`
  - `pipenv run python esptool.py --chip esp32c3 --port /dev/ttyACM0 --baud 921600 --before default_reset --after hard_reset --no-stub  write_flash --flash_mode dio --flash_freq 80m 0x0 ESP32_GENERIC_C3-20231005-v1.21.0.bin`
- Install rshell python package:
  - `pipenv install rshell`
- Connect to the esp32c3 chip using rshell:
  - `pipenv run rshell --baud 921600 -p /dev/ttyACM0`
