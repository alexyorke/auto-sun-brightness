import urllib
import urllib2
import json
import pytz
from dateutil.parser import parse
from datetime import datetime
from numpy import interp

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--lat', type=float, help='the latitude of your current location', required=True)
parser.add_argument('--long', type=float, help='the longitude of your current location', required=True)

parser.add_argument('--max', type=int, help='the maximum value for the brightest time of day', required=True)
parser.add_argument('--min', type=int, help='the minimum value for the darkest time of day', required=True)

solarEvents = ["sunrise", "solar_noon", "sunset", "civil_twilight_begin", "civil_twilight_end", "nautical_twilight_begin", "nautical_twilight_end", "astronomical_twilight_begin", "astronomical_twilight_end"]
parser.add_argument('--day_start', type=str, nargs='?', const='sunrise', help='values: ' + ", ".join(solarEvents))
parser.add_argument('--day_end', type=str, nargs='?', const='sunset', help='values: ' + ", ".join(solarEvents))

args = parser.parse_args()

# Parse command-line arguments
lowestIntensity  = int(args.min)
highestIntensity = int(args.max)

if lowestIntensity >= highestIntensity:
	print "Error: lowest intensity cannot be greater than the highest intensity"
	exit()

lat = float(args.lat)
lng = float(args.long)

turnOnLightsAfter = "sunrise"
if args.day_start is not None:
	turnOnLightsAfter = args.day_start

dimLightsBefore = "sunset"
if args.day_end is not None:
	dimLightsBefore = args.day_end


intensity = None

# get the sunrise/sunset data
url = 'http://api.sunrise-sunset.org/json?lat=' + str(lat) + "&lng=" + str(lng) + '&date=today&formatted=0'

data = urllib.urlopen(url).read()
decodeJson = json.loads(data)

# parse it
sunrise  = parse(decodeJson['results'][turnOnLightsAfter]).replace(tzinfo=pytz.utc)
sunset   = parse(decodeJson['results'][dimLightsBefore]).replace(tzinfo=pytz.utc)
currTime = datetime.utcnow().replace(tzinfo=pytz.utc)

secondsSunIsUp  = (sunset - sunrise).total_seconds()
timeFromSunrise = (currTime - sunrise).total_seconds()

# interpolate brightness depending on where the sun is in the sky from lowestIntensity to highestIntensity
if (secondsSunIsUp / 2) < timeFromSunrise: # past midday, start dimming lights
	intensity = highestIntensity - interp(timeFromSunrise, [secondsSunIsUp / 2, secondsSunIsUp], [lowestIntensity, highestIntensity])
else:
	intensity = interp(timeFromSunrise, [0,secondsSunIsUp / 2], [lowestIntensity, highestIntensity])

print intensity

# http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
# http://stackoverflow.com/questions/466345/converting-string-into-datetime
