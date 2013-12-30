#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NodeSite.settings")

    def welcome():
        return u"copyright: CSLG; version: v0.0.1"
    
    print welcome()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
