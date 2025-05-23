#! /usr/bin/env python3



codecs = [
    "h265 10bit",
    "h265",
    "h264"
]

codec_options = [
    "-pix_fmt yuv420p10le -c:v libx265 -x265-params profile=main10",
    "-c:v libx265 -x265-params profile=main10",
    "-c:v libx264"
]

presets = [
    "slow",
    "medium",
    "fast"
]

default_crf = 20

default_output_dir = "./renders-output"





# Prints the error string taken in input and terminates the script.

def errorr(s):
    print("ERROR: "+str(s)+". Exiting...")
    sys.exit(1)



# Ask the user to enter a number between 'minimum' and 'maximum' (included)
# if the user does not enter anything, the function returns the default

def askNumber(askStr, default, minimum, maximum):
    while True:
        x = input(askStr)

        if (len(x) == 0):
            return default

        if (x.isnumeric()):
            x = int(x)
            if (x >= minimum and x <= maximum):
                return x

        print("\nInvalid choice, retry")



# Gets in input a string that will be printed,
# and an array of strings (choices).
# Returns the chosen one. (default is 0)

def choice(askStr, options):
    l = len(options)
    while True:
        print(askStr)
        for i in range(l):
            print("\t"+str(i)+") "+options[i])

        x = input("\nEnter a number (default is 0): ")

        if (len(x) == 0):
            return 0
        if (x.isnumeric()):
            x = int(x)
            if (x >= 0 and x < l):
                return x

        print("\nInvalid choice, retry")





def main():
    c_codec = choice("\nSelect codec: ", codecs)

    c_preset = choice("\nSelect preset: ", presets)

    crf = askNumber("\nEnter CRF (default is 20): ", default_crf, 0, 51)


    print(c_codec)
    print(c_preset)
    print(crf)





if __name__ == '__main__':
    main()
