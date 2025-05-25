#! /usr/bin/env python3

import sys


help_message = """
USAGE: ffmpeg-wrapper [OPTIONS] inputFile1 ... inputFileN

OPTIONS:
    -d, --use-defaults    Do not ask the user for input, use defaults.
"""

codecs = {
    "h264"       : "-c:v libx264",
    "h265"       : "-c:v libx265 -x265-params profile=main10",
    "h265 10bit" : "-pix_fmt yuv420p10le -c:v libx265 -x265-params profile=main10"
}

presets = [
    "slow",
    "medium",
    "fast"
]

default_codec = "h265 10bit"

default_preset = "slow"

default_crf = 20

default_output_dir = "./renders-output"





# Prints the error string taken in input and terminates the script.

def errorr(s):
    print(f"ERROR: {s}. Exiting...")
    sys.exit(1)



# Ask the user via the 'ask_str' string
# to enter a number between 'minimum' and 'maximum' (included).
# If the user does not enter anything, the function returns the 'default'

def askNumber(ask_str, default, minimum, maximum):
    while True:
        x = input(ask_str)

        if (len(x) == 0):
            return default

        if (x.isnumeric()):
            x = int(x)
            if (x >= minimum and x <= maximum):
                return x

        print("\nInvalid choice, retry")



# Ask the user via the 'ask_str' string
# to choose between an array (or dictionary) of 'options'.
# Returns the choosen option, or the 'default' one.

def choice(ask_str, default, options):
    options = list(options)
    if (default not in options):
        errorr("Default option is not a valid option")

    while True:
        print(ask_str)

        for index, key in enumerate(options):
            if key == default:
                print(f"\t{index}) {key} (default)")
            else:
                print(f"\t{index}) {key}")

        x = input("\nEnter a number: ")

        if (len(x) == 0):
            return default
        if (x.isnumeric()):
            x = int(x)
            if (x >= 0 and x < len(options)):
                return options[x]

        print("\nInvalid choice, retry")





def main():

    if (len(sys.argv) > 1 and (sys.argv[1] == "--use-defaults" or sys.argv[1] == "-d")):
        use_defaults = True
        input_files = sys.argv[2:]
    else:
        use_defaults = False
        input_files = sys.argv[1:]

    if len(input_files) == 0:
        print(help_message, end="")
        sys.exit(1)




    c_codec = choice("\nSelect codec: ", default_codec, codecs)

    c_preset = choice("\nSelect preset: ", default_preset, presets)

    crf = askNumber("\nEnter CRF (default is 20): ", default_crf, 0, 51)


    print(c_codec)
    print(c_preset)
    print(crf)





if __name__ == '__main__':
    main()
