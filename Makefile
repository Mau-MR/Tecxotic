server:
	sudo chmod 666 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
	sudo chmod 666 /dev/ttyACM0
	python3 main.py
install:
	pip install -r requirements.txt

