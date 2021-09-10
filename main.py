# import urllib library
# import json
import sys
import signal
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
	global information
	global reversedpattern
	response = urlopen(url)

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
			print("Reverse pattern...[", reversedpattern.__str__(), "]")
			GPIO.output(18, GPIO.HIGH)
		else:
			print("Normal pattern...[", reversedpattern.__str__(), "]")
			GPIO.output(18, GPIO.LOW)
		print("Information: ",information )
		time.sleep(5)


def interrupthandler(signum, frame):
	print('Signal handler called with signal', signum)
	print('Cleaning up...')
	GPIO.cleanup(18)
	sys.exit()


information = ""
reversedpattern = False


if __name__ == "__main__":
	GPIO.setmode(GPIO.BCM)
	GPIO.setmode(GPIO.OUT)
	signal.signal(signal.SIGINT, interrupthandler)
	run()

