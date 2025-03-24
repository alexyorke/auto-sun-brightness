import urllib.request
import json
import pytz
from dateutil.parser import parse
from datetime import datetime
from numpy import interp
import argparse

def get_brightness(lat, lng, max_intensity, min_intensity, day_start="sunrise", day_end="sunset"):
    """
    Calculate the current brightness based on the sun's position.
    
    Args:
        lat (float): Latitude of the location
        lng (float): Longitude of the location
        max_intensity (int): Maximum brightness value
        min_intensity (int): Minimum brightness value
        day_start (str): When to consider the day starts
        day_end (str): When to consider the day ends
        
    Returns:
        float: The current brightness value
    """
    # Validate inputs
    if min_intensity >= max_intensity:
        raise ValueError("Lowest intensity cannot be greater than highest intensity")

    # Get the sunrise/sunset data
    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0'
    data = urllib.request.urlopen(url).read()
    decode_json = json.loads(data.decode('utf-8'))

    # Parse sunrise/sunset times
    sunrise = parse(decode_json['results'][day_start]).replace(tzinfo=pytz.utc)
    sunset = parse(decode_json['results'][day_end]).replace(tzinfo=pytz.utc)
    curr_time = datetime.utcnow().replace(tzinfo=pytz.utc)

    seconds_sun_is_up = (sunset - sunrise).total_seconds()
    time_from_sunrise = (curr_time - sunrise).total_seconds()

    # Interpolate brightness
    if (seconds_sun_is_up / 2) < time_from_sunrise:  # Past midday, start dimming lights
        intensity = max_intensity - interp(time_from_sunrise,
                                      [seconds_sun_is_up / 2, seconds_sun_is_up],
                                      [min_intensity, max_intensity])
    else:
        intensity = interp(time_from_sunrise, [0, seconds_sun_is_up / 2],
                                        [min_intensity, max_intensity])

    return intensity

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--lat', type=float,
                        help='the latitude of your current location',
                        required=True)
    parser.add_argument('--long', type=float,
                        help='the longitude of your current location',
                        required=True)
    parser.add_argument('--max', type=int,
                        help='the maximum value for the brightest time of day',
                        required=True)
    parser.add_argument('--min', type=int,
                        help='the minimum value for the darkest time of day',
                        required=True)

    solar_events = ["sunrise", "solar_noon", "sunset", "civil_twilight_begin",
                   "civil_twilight_end", "nautical_twilight_begin",
                   "nautical_twilight_end", "astronomical_twilight_begin",
                   "astronomical_twilight_end"]

    parser.add_argument('--day_start', type=str, nargs='?',
                        const='sunrise', help='values: ' + \
                        ", ".join(solar_events))

    parser.add_argument('--day_end', type=str, nargs='?',
                        const='sunset', help='values: ' + ", ".join(solar_events))

    args = parser.parse_args()
    
    try:
        brightness = get_brightness(
            args.lat, 
            args.long, 
            args.max, 
            args.min,
            args.day_start or "sunrise",
            args.day_end or "sunset"
        )
        print(brightness)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 