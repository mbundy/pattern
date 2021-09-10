# import urllib library
# import json
import atexit

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
	url = "https://datis.clowd.io/api/kvny"
	response = urlopen(url)

	# storing the JSON response
	# from url in data
	data_json = json.loads(response.read())

	# print the json response
	print(data_json)

	airport = data_json[0]
	datis = airport['datis']
	# print(datis)
	runwaystart: int = datis.find('LNDG AND DEPG')
	if runwaystart != -1:
		runwayend: int = datis[runwaystart:].find('.')
		landing = datis[runwaystart:runwaystart + runwayend]
		if landing.find('34') > 0:
			return True
		else:
			return False
	else:
		return False


def run():
	while True:
		if reversepattern():
			print("Reverse pattern...")
			GPIO.output(18, GPIO.HIGH)
		else:
			print("Normal pattern...")
			GPIO.output(18, GPIO.LOW)
		time.sleep(5)


def cleanup():
	GPIO.cleanup(18)


if __name__ == "__main__":
	GPIO.setmode(GPIO.BCM)
	GPIO.setmode(GPIO.OUT)
	atexit.register(cleanup)
	run()

