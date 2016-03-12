#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    ConDeBot.py
## Desc:    Un con de bot IRC.
##
## Author:  "Das" Franck Hochstaetter
## Version: 0.4 (11/03/2016)
##
## Dependencies : Python-forecastio (pip install python-forecastio)
##                  Python wrapper around the OpenWeatherMap API
##                GeoPy (pip install geopy)
##                  Python client for several popular geocoding web services.
##                Irc (pip install irc)


#Define globals
NAME        = 'ConDeBot'                            # Name
SHME        = 'CDB'                                 # Short Name
VERS        = '0.5'                                 # Version
CDB_PATH    = '../ConDeBot/'                        # Path to ConDeBot root directory

HELP = NAME + " v" + VERS + "\nUSAGE :\n" \
        + "!cdb coffee                  Serve some coffee\n" \
        + "!cdb kaamelott [-q ID]       Kaamelott quotes\n" \
        + "!cdb version                 Show CDB and Weechat Version\n" \
        + "!cdb weather CITY_NAME       Show the weather and temperature of CITY_NAME"

#Import modules with try and catch
try:
    import argparse
    import irc
    import irc.bot
    import irc.client
    import logging
    from logging.handlers import RotatingFileHandler
    import os
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)

# Import ConDeBot modules
from modules import kaamelott
from modules import coffee
from modules import weather


class CDB(irc.bot.SingleServerIRCBot):
    logger = logging.getLogger()
    server = ""

    #Bot Initialization
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
        self.logger.info("#------------------------------#")
        self.logger.info("Initialization of IRCBot Started")
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, "Con de Bot IRC")
        irc.client.ServerConnection.buffer_class.errors = 'replace'
        self.channel = channel
        self.server = server
        self.logger.info("Initialization of IRCBot Done")

    #Actions done when connected to IRC server
    def on_welcome(self, serv, ev):
        self.logger.info("Join server " + self.server)
        serv.join(self.channel)
        self.logger.info("Join channel " + self.channel)

    #Actions done when message is receive on public channel
    def on_pubmsg(self, serv, ev):
        self.do_command(serv, ev, True)

    #Actions done when message is receive on private channel
    def on_privmsg(self, serv, ev):
        self.do_command(serv, ev, False)

    #Actions to manage speak on public OR private channel
    def speak(self, serv, string, nick, public):
        for line in string.split("\n"):
            if (public):
                serv.privmsg(self.channel, line)
            else:
                serv.privmsg(nick, line)

    #Actions to manage log info on public OR private channel
    def log_info_command(self, string, public):
        if (public):
            self.logger.info(string + " in " + self.channel)
        else:
            self.logger.info(string + " via Private Message")

    #Actions to manage log warnings on public OR private channel
    def log_warn_command(self, string, public):
        if (public):
            self.logger.warn(string + " in " + self.channel)
        else:
            self.logger.warn(string + " via Private Message")

    #Actions to manage error warnings on public OR private channel
    def log_error_command(self, string, public):
        if (public):
            self.logger.error(string + " in " + self.channel)
        else:
            self.logger.error(string + " via Private Message")

    #Actions to execute commands
    def do_command(self, serv, ev, public):
        nick = ev.source.nick
        channel = self.connection
        command = ev.arguments[0];

        if (command.split(" ")[0] == "!cdb"):

            #Display help
            if (len(command.split(" ")) == 1 or command.split(" ")[1] == "help"):
                self.log_info_command("Help requested by " + nick, public)
                self.speak(serv, HELP, nick, public)
                return

            #Display bot's version
            if (command.split(" ")[1] == "version"):
                self.log_info_command("Version requested by " + nick, public)
                self.speak(serv, NAME + "'s version : " + VERS, nick, public)

            #Serve a delicious coffee (Module: "coffee")
            elif (command.split(" ")[1] in ["café", "cafe", "coffee"]):
                self.log_info_command("Coffee requested by " + nick, public)
                self.speak(serv, "Here " + nick + ", that's your coffee. " + coffee.quote(), nick, public)

            #Display a kaamelott quote (Module: "kaamelott")
            elif (command.split(" ")[1] in ["kaamelott"]):
                kaamelott.main(self, serv, command, nick, public)

            #Display the weather of the argument city (Module: "Weather)
            elif (command.split(" ")[1] in ["weather", "météo", "meteo"]):
                weather.main(self, serv, command, nick, public)

            #Set/Unset operators
            elif (command.split(" ")[1] in ["op", "deop"]):
                command #Do nothing for now

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
