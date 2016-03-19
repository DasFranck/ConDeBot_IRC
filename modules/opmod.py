#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME            = "ConDeBot"
OPS_FILE_PATH   = "jsonfiles/"
OPS_FILE        = OPS_FILE_PATH + "ops.json"


try:
    import json
    import os
    import shlex
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)



#Check if user is op (NOT LOGGED FUNCTION, meant to be use in the source code of CDB)
def isop(guy):
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return (guy.lower() in ops)
    else:
        return (False)


#Check if user is op (LOGGED FUNCTION, meant to be used via !cdb isop)
def isop_l(self, serv, guy, nick, public):
    self.log_info_command("Operator status of %s (%s) requested by %s" % (guy, isop(guy), nick), public)
    if (isop(guy)):
        self.speak(serv, "%s is an operator" % guy, guy, public)
    else:
        self.speak(serv, "%s is not an operator" % guy, nick, public)
    return


#Op user
def op_him(self, serv, guy, ops, nick, public):
    if (not isop(nick)):
        self.speak(serv, "You don't have the right to do that.", nick, public)
        self.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (guy, nick), public)
        return (ops)

    if (isop(guy)):
        self.speak(serv, "%s is already an operator" % guy, nick, public)
        self.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (guy, nick), public)
        return (ops)

    self.speak(serv, "%s has been added as operator" % guy, nick, public)
    self.log_info_command("Adding operator (%s) requested by %s, OK" % (guy, nick), public)
    ops.append(guy.lower())
    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    return (ops)


#Deop user
def deop_him(self, serv, guy, ops, nick, public):
    if (not isop(nick)):
        self.speak(serv, "You don't have the right to do that.", nick, public)
        self.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (guy, nick), public)
        return (ops)

    if (not isop(guy)):
        self.speak(serv, "%s is already not an operator" % guy, nick, public)
        self.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (guy, nick), public)
        return (ops)

    self.speak(serv, "%s has been removed from operator list" % guy, nick, public)
    self.log_info_command("Deleting operator (%s) requested by %s, OK" % (guy, nick), public)
    ops.remove(guy.lower())
    return (ops)


#Op user
def op_list(self, serv, ops, nick, public):
    self.log_info_command("Operator list requested by %s" % nick, public)
    string = "Operator list: "
    for op in ops:
        if (op == ops[-1]):
            string += "%s" % op
        else:
            string += "%s, " % op
    self.speak(serv, string, nick, public)
    return


#The main manager
def main(self, serv, command, nick, public):
    arglist = shlex.split(command)
    if (not os.path.exists(OPS_FILE_PATH)):
        os.makedirs(OPS_FILE_PATH)

    ops = []
    #If json file exist, load it
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)

    if (arglist[1] == "op"):
        for i in range(2, len(arglist)):
            ops = op_him(self, serv, arglist[i], ops, nick, public)
    if (arglist[1] == "deop"):
        for i in range(2, len(arglist)):
            ops = deop_him(self, serv, arglist[i], ops, nick, public)
    if (arglist[1] == "isop"):
        for i in range(2, len(arglist)):
            isop_l(self, serv, arglist[i], nick, public)
    if (arglist[1] == "list_op"):
        op_list(self, serv, ops, nick, public)

    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    return
