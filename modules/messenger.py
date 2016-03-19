#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME            = "ConDeBot"
MSG_FILE_PATH   = "jsonfiles/"
MSG_FILE        = OPS_FILE_PATH + "messenger.json"


try:
    import json
    import os
    import shlex
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)

#The main manager
def main(self, serv, command, nick, public):
    arglist = shlex.split(command)
    if (not os.path.exists(MSG_FILE_PATH)):
        os.makedirs(MSG_FILE_PATH)

    msg = []
    #If json file exist, load it
    if (os.path.isfile(MSG_FILE)):
        with open(MSG_FILE) as msg_file:
            msg = json.load(msg_file)

    if (len(arglist) == 1 and arglist[0] == "!c"):
        #PRINT USAGE
        return
    if (len(arglist) == 1 and arglist[0] == "!cl"):
        #SEND LIST OF TRIGGER MESSAGE
        return

    with open(MSG_FILE, 'w') as msg_file:
        json.dump(msg, msg_file)
    return
