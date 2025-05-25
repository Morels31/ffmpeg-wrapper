#! /usr/bin/env python3

import os
import sys


help_message = """
USAGE: ffmpeg-wrapper [OPTIONS] inputFile1 ... inputFileN

OPTIONS:
    -d, --use-defaults    Do not ask the user for input, use defaults.
"""

keep_container_string = "Keep the same"

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

containers = [
    keep_container_string
    "mp4"
    "mkv"
]

default_codec = "h265 10bit"

default_preset = "slow"

default_container = "mkv"

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



# Given an array of file paths in input,
# returns an array of the files that do not exists.

def checkFilesExistence(file_array):
    res = []
    for file in file_array:
        if (not os.path.isfile(file)):
            res.append(file)
    return res



# Given an array of file paths in input,
# returns an array of the files without the given 'permission'.
# 'permission' can be: os.R_OK, os.W_OK or os.X_OK

def checkFilesPermission(file_array, permission):
    res = []
    for file in file_array:
        if (not os.access(file, permission)):
            res.append(file)
    return res



# Given an array of file paths in input,
# checks if all the files exists and are readable,
# if not, throws an error and exits

def checkInputFiles(input_files):
    non_existent_files = checkFilesExistence(input_files)
    if (len(non_existent_files) > 0):
        print("ERROR: Some of the files given in input do not exists:", end="")
        for file in non_existent_files:
            print(f" \"{file}\"", end="")
        print(". Exiting...")
        sys.exit(1)

    non_readable_files = checkFilesPermission(input_files, os.R_OK)
    if (len(non_readable_files) > 0):
        print("ERROR: Some of the files given in input are not readable:", end="")
        for file in non_readable_files:
            print(f" \"{file}\"", end="")
        print(". Exiting...")
        sys.exit(1)



# Create the output directory if it doen't exists.
# Check write and execute permission if it does.

def createOutputDir(output_dir):
    if os.path.isdir(output_dir):
        if ((not os.access(output_dir, os.W_OK)) or (not os.access(output_dir, os.X_OK))):
            errorr("Cannot write to already existing output directory, permission denied")
    else:
        try:
            os.makedirs(output_dir)
        except Exception as e:
            errorr(e)



# Changes the file extension,
# returns the result

def changeExtension(file, new_ext):
    basename , _ = os.path.splitext(file)
    return basename + "." + new_ext





def main():

    if (len(sys.argv) > 1 and (sys.argv[1] == "--use-defaults" or sys.argv[1] == "-d")):
        use_defaults = True
        input_files = sys.argv[2:]
    else:
        use_defaults = False
        input_files = sys.argv[1:]


    if (len(input_files) == 0):
        print(help_message, end="")
        sys.exit(1)

    checkInputFiles(input_files)


    if use_defaults:
        codec = default_codec
        preset = default_preset
        container = default_container
        crf = default_crf
        output_dir = default_output_dir
    else:
        codec = choice("\nSelect codec: ", default_codec, codecs)
        preset = choice("\nSelect preset: ", default_preset, presets)
        container = choice("\nSelect container: ", default_container, containers)
        crf = askNumber("\nEnter CRF (default is 20): ", default_crf, 0, 51)
        output_dir = input("\nEnter output directory (or press ENTER for default): ")
        if (len(output_dir) == 0):
            output_dir = default_output_dir

    createOutputDir(output_dir)





if __name__ == '__main__':
    main()
