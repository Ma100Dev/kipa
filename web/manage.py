# TODO: Python3
#!/usr/bin/python2

import os, sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)

