#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    ConDeBot.py
## Desc:    Un con de bot IRC.
##
## Author:  "Das" Franck Hochstaetter
## Version: 0.3 (11/09/2015)

## Dependencies : Python-forecastio (pip2 install python-forecastio)
##                  Python wrapper around the OpenWeatherMap API
##                GeoPy (pip2 install geopy)
##                  Python client for several popular geocoding web services.

## cdb_buffer = buffer du bot
## chg_buffer = buffer choucroute_garnie (freenode)
## hook_cdb/con_de_bot = Hook pour l'appel du bot.


NAME        = 'ConDeBot'                            # Name
SHME        = 'CDB'                                 # Short Name
VERS        = '0.3'                                 # Version
WAPI        = "d9a2ec468ac33925d45017727ed4e499"    # Forecast.io API Key
CDB_PATH    = '../ConDeBot/'                        # Path to ConDeBot root directory

HELP = NAME + " v" + VERS + "\nUSAGE :\n" \
        + "!cdb kaamelott [-q ID]       Kaamelott quotes\n" \
        + "!cdb version                 Show CDB and Weechat Version\n" \
        + "!cdb weather CITY_NAME       Show the weather and temperature of CITY_NAME"


import_ok = True

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

try:
    import codecs
    import forecastio
    import random
    import shlex
    import sys
    import weechat
    from geopy.geocoders import Nominatim
    from ConDeBot.modules.kaamelott import *
    from ConDeBot.modules.weather import *
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    import_ok = False


def buffer_input_cb(data, buffer, input_data):
    return (weechat.WEECHAT_RC_OK)


def buffer_close_cb(data, buffer):
    return (weechat.WEECHAT_RC_OK)

## CDB_Version
# Display version of CDB and Weechat
def cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message):
    weechat.command(buffer, NAME + " version : " + VERS);
    weechat.command(buffer, "Weechat version : %s" % weechat.info_get("version", ""))
    weechat.prnt(data, "Version was requested by " + prefix + " at " + date + ".")
    return (weechat.WEECHAT_RC_OK)



## CDB_Coffee
# Coffee Sir.
def cmd_coffee(data, buffer, date, tags, displayed, highlight, prefix, message):
    weechat.command(buffer, "Here " + prefix + ", that's your coffee. Without sugar.")
    return (weechat.WEECHAT_RC_OK)


## CDB
# What do the bot says ?
def con_de_bot(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    print(arglist);
    if (len(arglist) == 1):
        weechat.command(buffer, HELP);
        weechat.prnt(data, "Help was? requested by " + prefix + " at " + date + ".")
        return (weechat.WEECHAT_RC_ERROR)
    elif (arglist[1] == "version"):
        return (cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message))
    elif (arglist[1] == "weather"):
        return (cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message))
    elif (arglist[1] == "kaamelott"):
        return (cmd_kaamelott(data, buffer, date, tags, displayed, highlight, prefix, message))
    elif (arglist[1] == "café" or arglist[1] == "cafe" or arglist[1] == "coffee"):
        return (cmd_coffee(data, buffer, date, tags, displayed, highlight, prefix, message))
    elif (arglist[1] == "help"):
        weechat.command(buffer, HELP);
        weechat.prnt(data, "Help was requested by " + prefix + " at " + date + ".")
    return (weechat.WEECHAT_RC_OK)


# The Main.
def main():
    weechat.register(NAME, "DasFranck", VERS, "Pro", NAME, "", "")
    weechat.command("", "/connect freenode")

    cdb_buffer = weechat.buffer_new("CDB_buffer", "buffer_input_cb", "", "buffer_close_cb", "")
    weechat.buffer_set(cdb_buffer, "title", "Console du " + NAME)

    chg_buffer = weechat.buffer_search("irc", "freenode.#choucroute-garnie")
    hook_cdb = weechat.hook_print(chg_buffer, "", "!cdb", 1, "con_de_bot", cdb_buffer)

    weechat.prnt(cdb_buffer, "Initialisation done.")


if __name__ == '__main__' and import_ok:
    main();
