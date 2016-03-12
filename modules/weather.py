#!/usr/bin/env python3
# -*- coding: utf-8 -*-


WAPI        = "d9a2ec468ac33925d45017727ed4e499"    # Forecast.io API Key


try:
    import forecastio
    from geopy.geocoders import Nominatim
    import shlex
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)



# Display weather of the city of arglist[2+]
def main(self, serv, command, nick, public):
    arglist = shlex.split(command)
    if (len(arglist) == 2):
        self.log_info_command("Weather's usage requested by " + nick, public)
        self.speak(serv, "Usage : !cdb weather CITY_NAME", nick, public)
        return

    geolocator = Nominatim();
    city_name = "";
    for i in range(2, len(arglist)):
        city_name += arglist[i] + " "

    city_name = city_name[:-1]
    loc = geolocator.geocode(city_name)
    forecast = forecastio.load_forecast(WAPI, loc.latitude, loc.longitude, units="si")
    current_weather = forecast.currently()
    self.speak(serv, "Weather : " + current_weather.summary, nick, public)
    self.speak(serv, "Temperature : " + str(current_weather.temperature) + " °C", nick, public)
    self.log_info_command("Weather of " + city_name + " was requested by " + nick, public)
    return
