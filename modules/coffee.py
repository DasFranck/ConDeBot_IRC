#!/usr/bin/env python3
# -*- coding: utf-8 -*-


NAME = "ConDeBot"
QUOTES = ["Without sugar.", "With one sugar.", "With too many sugar.",
          "With a pinch of sugar.", "With three spoon of salt because I hate you. Really.",
          "With a bit of milk.", "Wait did I put a sugar? I'm not sure...", ""]


try:
    # import json
    import random
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)


def quote():
    return (random.choice(QUOTES))
