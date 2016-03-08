#!/usr/bin/env python3

# Display random quotes of Kaamelott
def cmd_kaamelott_quote(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message)
    fd_kaam = codecs.open(CDB_PATH + "txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()

    nb = random.randint(1, int(buf[0:buf.index('\n')]))
    beg_quote = buf.find("#"+str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1

    weechat.prnt(data, "Random Kaamelott Quote (#" + str(nb) + ") was requested by " + prefix + " at " + date + ".")
    weechat.command(buffer, buf[beg_quote:end_quote])
    fd_kaam.close()
    return (weechat.WEECHAT_RC_OK)

## CDB_Kaamelott
# Display specific quotes of Kaamelott
def cmd_kaamelott_spec(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message)
    fd_kaam = codecs.open(CDB_PATH + "txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()

    if (len(arglist) == 3):
        weechat.command(buffer, "There's " + buf[0:buf.index('\n')] + "Kaamelott Quote")
        weechat.prnt(data, "Number of Kaamelott Quotes (" + buf[0:buf.index('\n')] + ") was requested by " + prefix + " at " + date + ".")
        fd_kaam.close()
        return (weechat.WEECHAT_RC_OK)

    nb = int(arglist[3]);
    if (nb > int(buf[0:buf.index('\n')])):
        weechat.command(buffer, "ERROR : Kaamelott Quote #" + str(nb) + " doesn't exist")
        weechat.prnt(data, "FAILED : Kaamelott Quote #" + str(nb) + " was requested by " + prefix + " at " + date + ".")
        fd_kaam.close()
        return (weechat.WEECHAT_RC_ERROR)

    beg_quote = buf.find("#"+str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1
    weechat.prnt(data, "Kaamelott Quote #" + str(nb) + " was requested by " + prefix + " at " + date + ".")
    weechat.command(buffer, buf[beg_quote:end_quote])
    fd_kaam.close()
    return (weechat.WEECHAT_RC_OK)

# Manage Kaamelott
def cmd_kaamelott(data, buffer, date, tags, displayed, highlight, prefix, message):
    arglist = shlex.split(message)
    if (len(arglist) == 2):
        return (cmd_kaamelott_quote(data, buffer, date, tags, displayed, highlight, prefix, message))
    elif (len(arglist) >= 3 and arglist[2] == "-q"):
        return (cmd_kaamelott_spec(data, buffer, date, tags, displayed, highlight, prefix, message))
    return (weechat.WEECHAT_RC_OK)
