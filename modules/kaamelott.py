#!/usr/bin/env python3

import shlex
import codecs
import random

# Display random quotes of Kaamelott
def quote(self, serv, message, nick, public):
    arglist = shlex.split(message)
    fd_kaam = codecs.open("txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()
    nb = random.randint(1, int(buf[0:buf.index('\n')]))
    beg_quote = buf.find("#"+str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1

    self.log_info_command("Random Kaamelott Quote (#" + str(nb) + ") was requested by " + nick, public)
    self.speak(serv, buf[beg_quote:end_quote], nick, public)
    fd_kaam.close()
    return (0)


# Display specific quotes of Kaamelott
def spec(self, serv, message, nick, public):
    arglist = shlex.split(message)
    fd_kaam = codecs.open("txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()

    if (len(arglist) == 3):
        self.log_info_command("Number of Kaamelott Quote (" + buf[0:buf.index('\n')] + ") was requested by " + nick, public)
        self.speak(serv, "There's " + buf[0:buf.index('\n')] + " Kaamelott Quote", nick, public)
        fd_kaam.close()
        return (0)

    nb = int(arglist[3]);
    if (nb > int(buf[0:buf.index('\n')])):
        self.log_warn_command("Non-existant Kaamelott Quote #" + str(nb) + " was requested by " + nick, public)
        self.speak(serv, "FAILED : Kaamelott Quote #" + str(nb) + " doesn't exist", nick, public)
        fd_kaam.close()
        return (1)

    beg_quote = buf.find("#"+str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1
    self.log_info_command("Kaamelott Quote #" + str(nb) + " was requested by " + nick, public)
    self.speak(serv, buf[beg_quote:end_quote], nick, public)
    fd_kaam.close()
    return (0)


# Manage Kaamelott
def main(self, serv, message, nick, public):
    arglist = shlex.split(message)
    if (len(arglist) == 2):
        return (quote(self, serv, message, nick, public))
    elif (len(arglist) >= 3 and arglist[2] == "-q"):
        return (spec(self, serv, message, nick, public))
    return (0)
