# auto-sun-brightness
Automatically change brightness of your lights depending on how bright the sun is

Usage: `python auto-sun-brightness.py`
Returns: a brightness float value (from min to max) which you can use to plug into your IoT lights.

**Important:** please change `lat` and `lng` in the python file to match your longitude and latitude, otherwise it will not work.

## Credits

This application uses sunrise-sunset.org's API: http://sunrise-sunset.org/api
