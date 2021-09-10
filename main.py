# import urllib library
# import json
import daemon
import time
import json
from urllib.request import urlopen
import importlib.util

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """

    import FakeRPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.OUT)

# store the URL in url as
# parameter for urlopen
url = "https://datis.clowd.io/api/kvny"

# store the response of URL
response = urlopen(url)

# storing the JSON response 
# from url in data
data_json = json.loads(response.read())

# print the json response
print(data_json)

airport = data_json[0]
datis = airport['datis']
#print(datis)
runwaystart: int = datis.find('LNDG AND DEPG')
#print(datis[runwaystart:])
runwayend: int = datis[runwaystart:].find('.')
landing = datis[runwaystart:runwaystart + runwayend]
if landing != -1:
    if landing.find('34') > 0:
        print("Reverse pattern...")
        GPIO.output(18, GPIO.HIGH)
    else:
        print("Normal pattern...")
        GPIO.output(18, GPIO.LOW)

GPIO.cleanup(18)
