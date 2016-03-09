#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

QUOTES = ["Without sugar.", "With one sugar.", "With too many sugar.",
          "With a pinch of sugar.", "With three spoon of salt because I hate you. Really.",
          "With a bit of milk.", "Wait did I put a sugar? I'm not sure...", ""]

def quote():
    return(random.choice(QUOTES))
