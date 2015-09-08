#!/usr/bin/env python

## Name:    HelloWorld.py
## Desc:    Testing script for Weechat Python API
##
## Author:  "Das" Franck Hochstaetter
## Version: vX

import weechat
import re
## cdb_buffer = buffer du bot
## chg_buffer = buffer choucroute_garnie (freenode)
## hook_cdb/con_de_bot = Hook pour l'appel du bot.

NAME = 'ConDeBot' # Name
SHME = 'CDB'      # Short Name
VERS = 'vX'       # Version

def buffer_input_cb(data, buffer, input_data):
    return (weechat.WEECHAT_RC_OK);

def buffer_close_cb(data, buffer):
    return (weechat.WEECHAT_RC_OK);

def cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message):
    weechat.command(buffer, NAME + " version : " + VERS);
    weechat.command(buffer, "Weechat version : %s" % weechat.info_get("version", ""));
    return (weechat.WEECHAT_RC_OK);

def con_de_bot(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = message.split(" ", message.count(" "));
    if (len(arglist) == 1):
        weechat.command(buffer, "Usage : No.");
    elif (arglist[1] == "version"):
        cmd_version(data, buffer, date, tags, displayed, highlight, prefix, message);
    return (weechat.WEECHAT_RC_OK);

def main():
    weechat.register(NAME, "DasFranck", "1.0 rev A", "Pro", NAME, "", "");
    weechat.command("", "/connect freenode");

    cdb_buffer = weechat.buffer_new("CDB_buffer", "buffer_input_cb", "", "buffer_close_cb", "");
    weechat.buffer_set(cdb_buffer, "title", "Console du " + NAME);
    weechat.prnt(cdb_buffer, "Done.");

    chg_buffer = weechat.buffer_search("irc", "freenode.#choucroute-garnie");
    hook_cdb = weechat.hook_print(chg_buffer, "", "!cdb", 1, "con_de_bot", cdb_buffer);

if __name__ == '__main__':
    main();
