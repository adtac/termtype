import os
import sys
import time

from distutils import spawn
from subprocess import call

def verify_deps(programs=["xdotool"]):
    prlist = ", ". join(programs)
    for program in programs:
        if spawn.find_executable(program) is None:
            print("Error: " + program + " not found.")
            print("Ensure that the following are installed: " + prlist)
            sys.exit(1)


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def main():
    verify_deps()
    if len(sys.argv) != 2:
        print("Usage: termtype <input_file>")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " does exist.")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = f.read().splitlines()

    segments = [[]]
    dividers = []
    for line in lines:
        if line == "":
            continue
        if line[0] == "<" and line[-1] == ">":
            segments.append([])
            dividers.append(line[1:-1])
        else:
            segments[-1].append(line)
    dividers.append("")

    for segment, divider in zip(segments, dividers):
        i = 0
        print(segment, divider)
        for line in segment:
            for char in line:
                call(["xdotool", "type", char])
                time.sleep(0.05)
            if i != len(segment) - 1:
                call(["xdotool", "key", "Return"])
            i += 1
        if divider.startswith("Sleep"):
            duration = float(divider.split(":")[1])/1000.0
            time.sleep(duration)
        else:
            call(["xdotool", "key", divider])

