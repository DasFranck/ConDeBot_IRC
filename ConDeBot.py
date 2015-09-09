#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Name:    HelloWorld.py
## Desc:    Testing script for Weechat Python API
##
## Author:  "Das" Franck Hochstaetter
## Version: 0.2 (09/09/2015)

## Dependencies : Python-forecastio (pip install python-forecastio)
##                  Python wrapper around the OpenWeatherMap API  
##                GeoPy (pip install geopy)
##                  Python client for several popular geocoding web services.

import weechat
import forecastio
from geopy.geocoders import Nominatim

## cdb_buffer = buffer du bot
## chg_buffer = buffer choucroute_garnie (freenode)
## hook_cdb/con_de_bot = Hook pour l'appel du bot.

NAME = 'ConDeBot'                           # Name
SHME = 'CDB'                                # Short Name
VERS = '0.2'                                # Version
WAPI = ""                                   # Weather API Key


def buffer_input_cb(data, buffer, input_data):
    return (weechat.WEECHAT_RC_OK);


def buffer_close_cb(data, buffer):
    return (weechat.WEECHAT_RC_OK);


# Display version of Weechat and CDB
def cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message):
    weechat.command(buffer, NAME + " version : " + VERS);
    weechat.command(buffer, "Weechat version : %s" % weechat.info_get("version", ""));
    weechat.prnt(data, "Version was requested by " + prefix + " at " + date + ".");
    return (weechat.WEECHAT_RC_OK);


# Dislay weather of the city of arglist[2]
def cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = message.split(" ", message.count(" "));
    if (len(arglist) == 2):
        weechat.command(buffer, "Usage : !cdb weather CITY_NAME");
        return (weechat.WEECHAT_RC_ERROR);
    geolocator = Nominatim();
    loc = geolocator.geocode(arglist[2]);
    forecast = forecastio.load_forecast(WAPI, loc.latitude, loc.longitude, units="si");
    current_weather = forecast.currently();
    weechat.command(buffer, "Weather : " + current_weather.summary);
    weechat.command(buffer, "Temperature : " + str(current_weather.temperature) + "C"); 
    return (weechat.WEECHAT_RC_OK);


# What do the bot says ?
def con_de_bot(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = message.split(" ", message.count(" "));
    if (len(arglist) == 1):
        weechat.command(buffer, "Usage : No.");
        return (weechat.WEECHAT_RC_ERROR);
    elif (arglist[1] == "version"):
        cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message);
    elif (arglist[1] == "weather"):
        cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message);
    return (weechat.WEECHAT_RC_OK);


# The Main.
def main():
    weechat.register(NAME, "DasFranck", VERS, "Pro", NAME, "", "");
    weechat.command("", "/connect freenode");

    cdb_buffer = weechat.buffer_new("CDB_buffer", "buffer_input_cb", "", "buffer_close_cb", "");
    weechat.buffer_set(cdb_buffer, "title", "Console du " + NAME);

    chg_buffer = weechat.buffer_search("irc", "freenode.#choucroute-garnie");
    hook_cdb = weechat.hook_print(chg_buffer, "", "!cdb", 1, "con_de_bot", cdb_buffer);

    weechat.prnt(cdb_buffer, "Initialisation done.");


if __name__ == '__main__':
    main();
