from __future__ import with_statement

import os
import sys

from ResponseBuilder import process
from MainWindow import MainWindow

argc = len(sys.argv)

def usage():
    sys.stdout.writelines([
        "Usage:\n",
        "\tperfect_abstraction.py - open windowed mode\n",
        "\tperfect_abstraction.py usage - show usage\n",
        "\tperfect_abstraction.py file inputfile outputfile - process input file and write to output\n",
        "\tperfect_abstraction.py stdin - process stdin data and write to stdout\n"
    ])


def open_windowed():
    MainWindow().show()


def open_file():
    if argc != 4:
        usage()
        return
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    if not os.path.exists(input_file_name):
        sys.stdout.write("Input file not found %s." % input_file_name)
        return

    input_file = open(input_file_name)
    data = input_file.read()
    result = process(data)

    output_file = open(output_file_name, 'w')
    output_file.write(result)
    output_file.close()


def open_std_input():
    data = sys.stdin.readlines()
    result = process("\n".join(data))
    sys.stdout.write(result)

OPERATIONS = {
    "usage": usage,
    "file": open_file,
    "stdin": open_std_input
}

if argc == 1:
    open_windowed()
elif argc > 1:
    operation = sys.argv[1]
    if operation not in OPERATIONS:
        usage()
    else:
        OPERATIONS[operation]()
