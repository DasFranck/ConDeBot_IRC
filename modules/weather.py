#!/usr/bin/env python3

## CDB_Weather
# Display weather of the city of arglist[2]
def cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message)
    if (len(arglist) == 2):
        weechat.command(buffer, "Usage : !cdb weather CITY_NAME")
        return (weechat.WEECHAT_RC_ERROR)
    geolocator = Nominatim();
    city_name = "";
    for i in range(2, len(arglist)):
        city_name += arglist[i]

    loc = geolocator.geocode(arglist[2])
    forecast = forecastio.load_forecast(WAPI, loc.latitude, loc.longitude, units="si")
    current_weather = forecast.currently()
    weechat.command(buffer, "Weather : " + current_weather.summary)
    weechat.command(buffer, "Temperature : " + str(current_weather.temperature) + " °C")
    weechat.prnt(data, "Weather of " + arglist[2] + " was requested by " + prefix + " at " + date + ".")
    return (weechat.WEECHAT_RC_OK)
