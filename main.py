# import urllib library
# import json
import sys
import signal
import atexit
from urllib.error import URLError

import daemon
import time
import json
from urllib.request import urlopen
import importlib.util

try:
	importlib.util.find_spec('RPi.GPIO')
	import RPi.GPIO as GPIO
except ImportError:
	import FakeRPi.GPIO as GPIO


# store the URL in url as
# parameter for urlopen
def reversepattern():
	# store the response of URL
	url = "https://zdatis.clowd.io/api/kvny"
	global information
	global reversedpattern
	try:
		response = urlopen(url)
	except URLError as e:
		if hasattr(e, 'reason'):
			print('We failed to reach a server.')
			print('Reason: ', e.reason)
		elif hasattr(e, 'code'):
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)
	else:
		# storing the JSON response
		# from url in data
		data_json = json.loads(response.read())

		# print the json response
		print(data_json)

		airport = data_json[0]
		datis = airport['datis']
		# print(datis)

		infostart: int = datis.find("INFO")
		information = datis[infostart + 5]

		runwaystart: int = datis.find('LNDG AND DEPG')
		if runwaystart != -1:
			runwayend: int = datis[runwaystart:].find('.')
			landing = datis[runwaystart:runwaystart + runwayend]
			if landing.find('34') > 0:
				reversedpattern = True
				return True
			else:
				reversedpattern = False
				return False
		else:
			return False


def run():
	while True:
		if reversepattern():
			print("Reverse pattern...")
			GPIO.output(8, GPIO.HIGH)
		else:
			print("Normal pattern...")
			GPIO.output(8, GPIO.LOW)
		print("Information: ",information )
		time.sleep(5)


def interrupthandler(signum, frame):
	print('Signal handler called with signal', signum)
	GPIO.output(8, GPIO.HIGH)
	time.sleep(0.25)
	GPIO.output(8, GPIO.LOW)
	print('Cleaning up...')
	GPIO.cleanup(8)
	sys.exit()


def gpiosetup(pin):
	GPIO.setwarnings(False)  # Ignore warning for now
	GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
	GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
	GPIO.output(8, GPIO.HIGH)
	time.sleep(0.25)
	GPIO.output(8, GPIO.LOW)


information = ""
reversedpattern = False


if __name__ == "__main__":
	gpiosetup(8)
	signal.signal(signal.SIGINT, interrupthandler)
	run()
