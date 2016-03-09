#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    ConDeBot.py
## Desc:    Un con de bot IRC.
##
## Author:  "Das" Franck Hochstaetter
## Version: 0.3nw (09/03/2016)

## Dependencies : Python-forecastio (pip install python-forecastio)
##                  Python wrapper around the OpenWeatherMap API
##                GeoPy (pip install geopy)
##                  Python client for several popular geocoding web services.
##                Irc (pip install irc)


NAME        = 'ConDeBot'                            # Name
SHME        = 'CDB'                                 # Short Name
VERS        = '0.3nw'                               # Version
WAPI        = "d9a2ec468ac33925d45017727ed4e499"    # Forecast.io API Key
CDB_PATH    = '../ConDeBot/'                        # Path to ConDeBot root directory

HELP = NAME + " v" + VERS + "\nUSAGE :\n" \
        + "!cdb kaamelott [-q ID]       Kaamelott quotes\n" \
        + "!cdb version                 Show CDB and Weechat Version\n" \
        + "!cdb weather CITY_NAME       Show the weather and temperature of CITY_NAME"

try:
    import argparse
    import codecs
    import forecastio
    from geopy.geocoders import Nominatim
    import irc
    import irc.bot
    import irc.client
    import logging
    from logging.handlers import RotatingFileHandler
    import os
    import random
    import shlex
    import sys
    from time import gmtime, strftime
#    from ConDeBot.modules.weather import *
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)

#from modules import kaamelott
from modules import coffee


class CDB(irc.bot.SingleServerIRCBot):
    logger = logging.getLogger()
    server = ""

    def __init__(self, server, port, channel, nickname):
        #Set logger level to INFO (almost all)
        self.logger.setLevel(logging.INFO)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        #Setting file_handler
        file_handler = RotatingFileHandler("logs/" + server + "-" + channel + ".log", 'a')
        file_handler.setFormatter(logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s"))
        self.logger.addHandler(file_handler)

        #Setting stream_handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)

        #Init IRCBot
        self.logger.info("Initialization of IRCBot Started")
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, "Con de Bot IRC")
        irc.client.ServerConnection.buffer_class.errors = 'replace'
        self.channel = channel
        self.server = server
        self.logger.info("Initialization of IRCBot Done")

    def on_welcome(self, serv, ev):
        self.logger.info("Join server " + self.server)
        serv.join(self.channel)
        self.logger.info("Join channel " + self.channel)

    def on_pubmsg(self, serv, ev):
        self.do_command(serv, ev, True)

    def on_privmsg(self, serv, ev):
        self.do_command(serv, ev, False)

    def speak(self, serv, string, nick, public):
        if (public):
            serv.privmsg(self.channel, string)
        else:
            serv.privmsg(nick, string)

    def log_info_command(self, string, public):
        if (public):
            self.logger.info(string + " in " + self.channel)
        else:
            self.logger.info(string + " via Private Message")

    def do_command(self, serv, ev, public):
        nick = ev.source.nick
        channel = self.connection

        if (ev.arguments[0].split(" ")[0] == "!cdb"):
            if (len(ev.arguments[0].split(" ")) == 1):
                self.log_info_command("Help requested by " + ev.source.split("!")[0], public)
                for line in HELP.split("\n"):
                    self.speak(serv, line, nick, public)
                return

            if (ev.arguments[0].split(" ")[1] == "version"):
                self.log_info_command("Version requested by " + ev.source.split("!")[0], public)
                self.speak(serv, NAME + " version : " + VERS, nick, public)

            elif (ev.arguments[0].split(" ")[1] in ["café", "cafe", "coffee"]):
                self.log_info_command("Coffee requested by " + ev.source.split("!")[0], public)
                self.speak(serv, "Here " + nick + ", that's your coffee. " + coffee.quote(), nick, public)



# The Main.
def main():
    parser = argparse.ArgumentParser(description="ConDeBot - Un con de bot IRC")
    parser.add_argument("-s", "--server", default="irc.freenode.com")
    parser.add_argument("-p", "--port", default="6667", type=int)
    parser.add_argument("-c", "--channel", default="#testmybot", type=str)
    parser.add_argument("-n", "--nickname", default="ConDeBot")
    args = parser.parse_args()

    CDB(args.server, args.port, args.channel, args.nickname).start()


if __name__ == '__main__':
    main();
