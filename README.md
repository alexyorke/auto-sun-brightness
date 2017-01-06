# auto-sun-brightness
Get a numeric representation of how bright the sun is at any point in the day, anywhere

```bash
usage: brightness.py [-h] --lat LAT --long LONG --max MAX --min MIN
                     [--day_start [DAY_START]] [--day_end [DAY_END]]

optional arguments:
  -h, --help            show this help message and exit
  --lat LAT             the latitude of your current location
  --long LONG           the longitude of your current location
  --max MAX             the maximum value for the brightest time of day
  --min MIN             the minimum value for the darkest time of day
  --day_start [DAY_START]
                        values: sunrise, solar_noon, sunset,
                        civil_twilight_begin, civil_twilight_end,
                        nautical_twilight_begin, nautical_twilight_end,
                        astronomical_twilight_begin, astronomical_twilight_end
  --day_end [DAY_END]   values: sunrise, solar_noon, sunset,
                        civil_twilight_begin, civil_twilight_end,
                        nautical_twilight_begin, nautical_twilight_end,
                        astronomical_twilight_begin, astronomical_twilight_end
```

Example: `python auto-sun-brightness.py --lat -10.15550 --long 75.67612 --max 10 --min 0`

Returns: a brightness float value (from min to max, which you can use to plug into your IoT lights for example.)


## Credits

This application uses sunrise-sunset.org's API: http://sunrise-sunset.org/api

http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another

http://stackoverflow.com/questions/466345/converting-string-into-datetime
