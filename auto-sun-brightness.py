import urllib
import urllib2
import json
import pytz
from dateutil.parser import parse
from datetime import datetime
from numpy import interp

# Configuration

lowestIntensity  = 0   # the lowest brightness the lights can get
highestIntensity = 100 # the brightest the lights can get
lat = None             # your latitude (e.g -57.52533)
lng = None             # your longitude (e.g -1.38363)

# Valid values:
# sunrise, sunset
# civil_twilight_begin, civil_twilight_end
# nautical_twilight_begin, nautical_twilight_end
# astronomical_twilight_begin, astronomical_twilight_end

turnOnLightsAfter = 'sunrise'
dimLightsBefore   = 'sunset'

# End configuration

intensity = 0

# get the sunrise/sunset data
url = 'http://api.sunrise-sunset.org/json?lat=' + str(lat) + "&lng=" + str(lng) + '&date=today&formatted=0'

data = urllib.urlopen(url).read()
decodeJson = json.loads(data)

# parse it
sunrise  = parse(decodeJson['results'][turnOnLightsAfter]).replace(tzinfo=pytz.utc)
sunset   = parse(decodeJson['results'][dimLightsBefore]).replace(tzinfo=pytz.utc)
currTime = datetime.utcnow().replace(tzinfo=pytz.utc)

secondsSunIsUp = -(sunrise - sunset).total_seconds()
timeFromSunrise = (currTime-sunrise).total_seconds()

# interpolate brightness depending on where the sun is in the sky from lowestIntensity to highestIntensity
if (secondsSunIsUp / 2) < timeFromSunrise: # past midday, start dimming lights
	intensity = highestIntensity - interp(timeFromSunrise, [secondsSunIsUp / 2, secondsSunIsUp], [lowestIntensity, highestIntensity])
else:
	intensity = interp(timeFromSunrise, [0,secondsSunIsUp / 2], [lowestIntensity, highestIntensity])

print intensity

# http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
# http://stackoverflow.com/questions/466345/converting-string-into-datetime
