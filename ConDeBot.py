#!/usr/bin/env python
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


NAME = 'ConDeBot'                           # Name
SHME = 'CDB'                                # Short Name
VERS = '0.3'                                # Version
WAPI = ""                                   # Forecast.io API Key

HELP = NAME + " v" + VERS + "\nUSAGE :\n" \
        + "!cdb kaamelott [-q nb]       Kaamelott quotes\n" \
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
    import weechat
    from geopy.geocoders import Nominatim
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    import_ok = False


def buffer_input_cb(data, buffer, input_data):
    return (weechat.WEECHAT_RC_OK);


def buffer_close_cb(data, buffer):
    return (weechat.WEECHAT_RC_OK);


# Display random quotes of Kaamelott
def cmd_kaamelott_quote(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    fd_kaam = codecs.open("kaamelott.txt", "r", "utf-8");
    buf = fd_kaam.read();

    nb = random.randint(1, int(buf[0:buf.index('\n')]));
    beg_quote = buf.find("#"+str(nb));
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1;

    weechat.prnt(data, "Random Kaamelott Quote (#" + str(nb) + ") was requested by " + prefix + " at " + date + ".");
    weechat.command(buffer, buf[beg_quote:end_quote]);
    fd_kaam.close();
    return (weechat.WEECHAT_RC_OK);

# Display specific quotes of Kaamelott
def cmd_kaamelott_spec(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    fd_kaam = codecs.open("kaamelott.txt", "r", "utf-8");
    buf = fd_kaam.read();

    if (len(arglist) == 3):
        weechat.command(buffer, "There's " + buf[0:buf.index('\n')] + "Kaamelott Quote"); 
        weechat.prnt(data, "Number of Kaamelott Quotes (" + buf[0:buf.index('\n')] + ") was requested by " + prefix + " at " + date + ".");
        fd_kaam.close();
        return (weechat.WEECHAT_RC_OK);

    nb = int(arglist[3]);
    if (nb > int(buf[0:buf.index('\n')])):
        weechat.command(buffer, "ERROR : Kaamelott Quote #" + str(nb) + " doesn't exist");
        weechat.prnt(data, "FAILED : Kaamelott Quote #" + str(nb) + " was requested by " + prefix + " at " + date + ".");
        fd_kaam.close();
        return (weechat.WEECHAT_RC_ERROR);

    beg_quote = buf.find("#"+str(nb));
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1;
    weechat.prnt(data, "Kaamelott Quote #" + str(nb) + " was requested by " + prefix + " at " + date + ".");
    weechat.command(buffer, buf[beg_quote:end_quote]);
    fd_kaam.close();
    return (weechat.WEECHAT_RC_OK);

# Manage Kaamelott
def cmd_kaamelott(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    if (len(arglist) == 2):
        return (cmd_kaamelott_quote(data, buffer, date, tags, displayed, highlight, prefix, message));
    elif (len(arglist) >= 3 and arglist[2] == "-q"):
        return (cmd_kaamelott_spec(data, buffer, date, tags, displayed, highlight, prefix, message));
    return (weechat.WEECHAT_RC_OK);


# Display version of CDB and Weechat
def cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message):
    weechat.command(buffer, NAME + " version : " + VERS);
    weechat.command(buffer, "Weechat version : %s" % weechat.info_get("version", ""));
    weechat.prnt(data, "Version was requested by " + prefix + " at " + date + ".");
    return (weechat.WEECHAT_RC_OK);


# Display weather of the city of arglist[2]
def cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    if (len(arglist) == 2):
        weechat.command(buffer, "Usage : !cdb weather CITY_NAME");
        return (weechat.WEECHAT_RC_ERROR);
    geolocator = Nominatim();
    loc = geolocator.geocode(arglist[2]);
    forecast = forecastio.load_forecast(WAPI, loc.latitude, loc.longitude, units="si");
    current_weather = forecast.currently();
    weechat.command(buffer, "Weather : " + current_weather.summary);
    weechat.command(buffer, "Temperature : " + str(current_weather.temperature) + "C"); 
    weechat.prnt(data, "Weather of " + arglist[2] + " was requested by " + prefix + " at " + date + ".");
    return (weechat.WEECHAT_RC_OK);


# What do the bot says ?
def con_de_bot(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message);
    print(arglist);
    if (len(arglist) == 1):
        weechat.command(buffer, HELP);
        weechat.prnt(data, "Help was? requested by " + prefix + " at " + date + ".");
        return (weechat.WEECHAT_RC_ERROR);
    elif (arglist[1] == "version"):
        return (cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message));
    elif (arglist[1] == "weather"):
        return (cmd_weather(data, buffer, date, tags, displayed, highlight, prefix, message));
    elif (arglist[1] == "kaamelott"):
        return (cmd_kaamelott(data, buffer, date, tags, displayed, highlight, prefix, message));
    elif (arglist[1] == "help"):
        weechat.command(buffer, HELP);
        weechat.prnt(data, "Help was requested by " + prefix + " at " + date + ".");

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


if __name__ == '__main__' and import_ok:
    main();
