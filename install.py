#!/usr/bin/env python3

import re

SE_INPUT = "se"
SE_OUTPUT = "/usr/share/X11/xkb/symbols/se"

EVDEV_XML_INPUT = "evdev.xml"
EVDEV_XML_OUTPUT = "/usr/share/X11/xkb/rules/evdev.xml"

EVDEV_LST_INPUT = "evdev.lst"
EVDEV_LST_OUTPUT = "/usr/share/X11/xkb/rules/evdev.lst"

print(f"Patching \"{SE_OUTPUT}\"...")

with open(SE_INPUT, "r") as fd:
    input_lines = fd.readlines()

with open(SE_OUTPUT, "a") as fd:
    fd.write("\n")
    fd.writelines(input_lines)

print(f"Patching \"{EVDEV_XML_OUTPUT}\"...")

insert_index = 0
with open(EVDEV_XML_OUTPUT, "r") as fd:
    output_lines = fd.readlines()
    output_lines_it = iter(output_lines)
    for i, line in enumerate(output_lines_it):
        if re.search("<iso639Id>swe</iso639Id>", line):
            # We found the Swedish layouts. Next find the start of the variant
            # list.
            while not re.search("<variantList>", line):
                line = next(output_lines_it)
                i += 1

            insert_index = i + 1
            break

assert(insert_index)

with open(EVDEV_XML_INPUT, "r") as fd:
    output_lines[insert_index:insert_index] = fd.readlines()

with open(EVDEV_XML_OUTPUT, "w") as fd:
    fd.writelines(output_lines)

print(f"Patching \"{EVDEV_LST_OUTPUT}\"...")

insert_index = 0
with open(EVDEV_LST_OUTPUT, "r") as fd:
    output_lines = fd.readlines()
    for i, line in enumerate(output_lines):
        if re.search(r"\s+se:\s+", line):
            # We found the Swedish variants.
            insert_index = i
            break

assert(insert_index)

with open(EVDEV_LST_INPUT, "r") as fd:
    output_lines[insert_index:insert_index] = fd.readline()

with open(EVDEV_LST_OUTPUT, "w") as fd:
    fd.writelines(output_lines)

print("usse sucessfully installed")
