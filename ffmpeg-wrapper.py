#! /usr/bin/env python3

import os
import sys
import subprocess


help_message = """
USAGE: ffmpeg-wrapper [OPTIONS] inputFile1 ... inputFileN

OPTIONS:
    -d, --use-defaults    Do not ask the user for input, use defaults.
"""

keep_container_string = "Keep the same"

custom_ffmpeg_ret_code = 67108097117100105111

codecs = {
    "h264"       : ["-c:v", "libx264"],
    "h265"       : ["-c:v", "libx265", "-x265-params", "profile=main10"],
    "h265 10bit" : ["-pix_fmt", "yuv420p10le", "-c:v", "libx265", "-x265-params", "profile=main10"]
}

presets = [
    "slower",
    "slow",
    "medium",
    "fast",
    "ultrafast"
]

containers = [
    keep_container_string,
    "mp4",
    "mkv"
]

default_codec = "h265 10bit"

default_preset = "slow"

default_container = "mkv"

default_crf = 20

default_output_dir = "./renders-output"

default_overwrite_existing_output = True

default_continue = True





# Prints the error string taken in input and terminates the script.

def errorr(s):
    print(f"\nERROR: {s}. Exiting...")
    sys.exit(1)



# Ask the user via the 'ask_str' string
# to enter "y" (yes) or "n" (no), and returns corrispectively True or False,
# if the user input is empty returns the 'default' boolean.

def askYesNo(ask_str, default):
    while True:
        x = input(f"{ask_str} [{"Y/n" if default else "y/N"}]: ")

        if (len(x) == 0):
            return default

        if x.lower() == "y":
            return True
        if x.lower() == "n":
            return False

        print("\nInvalid choice, retry")



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
# to choose between an array of 'options'.
# Returns the choosen option, or the 'default' one.

def choice(ask_str, default, options):
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



# Given an array in input,
# it returns only the unique values, in the original order.

def getUniqueValues(array):
    res = []
    for i in array:
        if i not in res:
            res.append(i)
    return res



# Given an array of file paths in input,
# returns a tuple containing two array,
# the first with the files that do exist,
# the second with the ones that do not.

def checkFilesExistence(file_array):
    existent_files = []
    non_existent_files = []

    for file in file_array:
        if os.path.isfile(file):
            existent_files.append(file)
        else:
            non_existent_files.append(file)

    return existent_files, non_existent_files



# Given an array of file paths in input,
# returns an array of the files without the given 'permission'.
# 'permission' can be: os.R_OK, os.W_OK or os.X_OK

def checkFilesPermission(file_array, permission):
    valid_perm_files = []
    invalid_perm_files = []

    for file in file_array:
        if os.access(file, permission):
            valid_perm_files.append(file)
        else:
            invalid_perm_files.append(file)

    return valid_perm_files, invalid_perm_files



# Given an array of file paths in input,
# checks if all the files do not start with ".." exists and are readable,
# if not, throws an error and exits

def checkInputFiles(input_files):
    for file in input_files:
        if file.startswith(".."):
            errorr("An input file cannot start with \"..\" it would break output directory structure")

    _, non_existent_files = checkFilesExistence(input_files)
    if (len(non_existent_files) > 0):
        errorr(f"Some of the files given in input do not exists: \"{'" "'.join(non_existent_files)}\"")

    _, non_readable_files = checkFilesPermission(input_files, os.R_OK)
    if (len(non_readable_files) > 0):
        errorr(f"Some of the files given in input are not readable: \"{'" "'.join(non_readable_files)}\"")



# Given an array of file paths in input,
# checks if all the files are unique,
# asks the user if to overwrite or not,
# and if files to be overwritten are writable.
# if not, throws an error and exits

def checkOutputFiles(output_files):
    tmp_set = set(output_files)
    if (len(tmp_set) != len(output_files)):
        errorr("Some input files generate the same output file")

    existent_output_files, _ = checkFilesExistence(output_files)
    if (len(existent_output_files)>0):
        print(f"\nWARNING: Continuing those files will be overwrited: \n\t\"{'"\n\t"'.join(existent_output_files)}\"\n")

        if not askYesNo("Continue?", default_overwrite_existing_output):
            sys.exit(1)

        _, non_writable_files = checkFilesPermission(output_files, os.W_OK)
        if (len(non_writable_files) > 0):
            print(f"\nERROR: Some of the files given in input are not writable: \n\t\"{'"\n\t"'.join(non_writable_files)}\"\n\nExiting...")
            sys.exit(1)



# Create the directory recursively if it doesn't exists.
# Check write and execute permission if it does.

def createDirectory(directory):
    if os.path.isdir(directory):
        if ((not os.access(directory, os.W_OK)) or (not os.access(directory, os.X_OK))):
            errorr("Cannot write to already existing directory, permission denied")
    else:
        try:
            os.makedirs(directory)
        except Exception as e:
            errorr(e)



# Changes the file extension,
# returns the result

def changeExtension(file, new_ext):
    basename , _ = os.path.splitext(file)
    return basename + "." + new_ext



# Execute ffmpeg in a subprocess,
# 'options' is an array of arguments that will be given to ffmpeg.
# Returns the return code of the called process.

def ffmpegRender(input_file, output_file, options):

    command = ["ffmpeg", "-i", input_file] + options + [ output_file ]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        while True:
            line = process.stdout.readline()
            if not line:
                break

            if line.strip().startswith("frame"):
                print(f"\r{line.rstrip()}", end="", flush=True)
            #else:
            #    log(line)

        print()
        return process.wait()

    except Exception as e:

        try:
            process.kill()
        except:
            pass

        print(f"ERROR: Failed rendering \"{input_file}\". Exception: {e}. Continuing anyway...")
        return custom_ffmpeg_ret_code





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


    input_files = [ os.path.normpath(file) for file in input_files ]
    input_files = getUniqueValues(input_files)

    checkInputFiles(input_files)


    if use_defaults:
        codec = default_codec
        preset = default_preset
        container = default_container
        crf = default_crf
        output_dir = default_output_dir
    else:
        codec = choice("\nSelect codec: ", default_codec, list(codecs))
        preset = choice("\nSelect preset: ", default_preset, presets)
        container = choice("\nSelect container: ", default_container, containers)
        crf = askNumber("\nEnter CRF (default is 20): ", default_crf, 0, 51)
        output_dir = input("\nEnter output directory (or press ENTER for default): ")
        if (len(output_dir) == 0):
            output_dir = default_output_dir

    ffmpeg_options = codecs[codec] + ["-preset", preset, "-crf", str(crf), "-y"]


    createDirectory(output_dir)


    if (container == keep_container_string):
        inputToOutput = lambda input_file, output_dir, container : os.path.normpath(os.path.join(output_dir, input_file))
    else:
        inputToOutput = lambda input_file, output_dir, container : os.path.normpath(os.path.join(output_dir, changeExtension(input_file, container)))

    output_files = []
    for input_file in input_files:

        output_file = inputToOutput(input_file, output_dir, container)

        if (output_file in input_files):
            errorr(f"The output file: \"{output_file}\" cannot overwrite an input file")

        createDirectory(os.path.dirname(output_file))
        output_files.append(output_file)


    checkOutputFiles(output_files)


    print("\nFiles summary:")
    for input_file, output_file in zip(input_files, output_files):
        print(f"\t{input_file} --> {output_file}")

    print("\nSettings summary:")
    print(f"\tCodec: \"{codec}\"\n\tPreset: \"{preset}\"\n\tCRF: \"{crf}\"\n\tContainer: \"{container}\"")


    if not askYesNo("\nContinue?", default_continue):
        sys.exit(1)

    failed_renders = []
    for input_file, output_file in zip(input_files, output_files):

        print(f"\nRendering: {input_file}\n")
        ret_code = ffmpegRender(input_file, output_file, ffmpeg_options)

        if (ret_code != 0):
            if (ret_code != custom_ffmpeg_ret_code):
                print(f"\nERROR: Failed rendering {input_file}. Continuing anyway...")
            failed_renders.append(input_file)
            try:
                os.remove(output_file)
            except:
                pass


    print("\n\nScript finished.")





if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(1)
    except Exception:
        raise
