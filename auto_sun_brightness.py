import argparse
import json
import urllib.request
from datetime import datetime

import pytz
from dateutil.parser import parse
from numpy import interp


SOLAR_EVENTS = [
    "sunrise",
    "solar_noon",
    "sunset",
    "civil_twilight_begin",
    "civil_twilight_end",
    "nautical_twilight_begin",
    "nautical_twilight_end",
    "astronomical_twilight_begin",
    "astronomical_twilight_end",
]


def get_brightness(
    lat,
    lng,
    max_intensity,
    min_intensity,
    day_start="sunrise",
    day_end="sunset",
):
    if min_intensity >= max_intensity:
        raise ValueError("min_intensity must be less than max_intensity")

    url = (
        "https://api.sunrise-sunset.org/json?lat="
        + str(lat)
        + "&lng="
        + str(lng)
        + "&date=today&formatted=0"
    )

    data = urllib.request.urlopen(url).read()
    decoded = json.loads(data.decode("utf-8"))

    sunrise = parse(decoded["results"][day_start]).replace(tzinfo=pytz.utc)
    sunset = parse(decoded["results"][day_end]).replace(tzinfo=pytz.utc)
    current_time = datetime.utcnow().replace(tzinfo=pytz.utc)

    seconds_sun_is_up = float((sunset - sunrise).total_seconds())
    time_from_sunrise = float((current_time - sunrise).total_seconds())

    if (seconds_sun_is_up / 2) < time_from_sunrise:
        return max_intensity - interp(
            time_from_sunrise,
            [seconds_sun_is_up / 2, seconds_sun_is_up],
            [min_intensity, max_intensity],
        )

    return interp(
        time_from_sunrise,
        [0, seconds_sun_is_up / 2],
        [min_intensity, max_intensity],
    )


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lat",
        type=float,
        help="the latitude of your current location",
        required=True,
    )
    parser.add_argument(
        "--long",
        type=float,
        help="the longitude of your current location",
        required=True,
    )
    parser.add_argument(
        "--max",
        type=int,
        help="the maximum value for the brightest time of day",
        required=True,
    )
    parser.add_argument(
        "--min",
        type=int,
        help="the minimum value for the darkest time of day",
        required=True,
    )
    parser.add_argument(
        "--day_start",
        type=str,
        nargs="?",
        const="sunrise",
        help="values: " + ", ".join(SOLAR_EVENTS),
    )
    parser.add_argument(
        "--day_end",
        type=str,
        nargs="?",
        const="sunset",
        help="values: " + ", ".join(SOLAR_EVENTS),
    )
    return parser


def main():
    args = build_parser().parse_args()
    intensity = get_brightness(
        lat=args.lat,
        lng=args.long,
        max_intensity=args.max,
        min_intensity=args.min,
        day_start=args.day_start or "sunrise",
        day_end=args.day_end or "sunset",
    )
    print(intensity)


if __name__ == "__main__":
    main()
