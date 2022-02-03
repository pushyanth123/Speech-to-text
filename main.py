#!/bin/python3

import sys
import argparse
import audio_from_file
import audio_from_mic


def main():
    parser = argparse.ArgumentParser(
        description="Script to convert speech to text")
    parser.add_argument(
        '-i', '--input', help='Input file (\'-\' To read file name from stdin)', required=False, metavar="")
    parser.add_argument(
        '-o', '--output', help='Output file (\'-\' To output into stdout)', required=False, metavar="")
    parser.add_argument(
        '-f', '--offline', help='Offline mode', required=False, action='store_true')
    args = parser.parse_args()

    if args.input == '-':
        input_file = sys.stdin.readline().strip()
    else:
        input_file = args.input

    text = ""

    # If "input" argument is not given, read from microphone
    is_quite = False if args.output == '-' or args.output == None else True

    if input_file == None:
        inp = audio_from_mic.FromMicrophone()
        inp.listen(2)
        # Convert speech to text
        text = inp.recognize_audio(quite=is_quite)
    else:
        inp = audio_from_file.FromAudioFile(input_file)
        # Convert speech to text
        text = inp.recognize_audio(quite=is_quite)

    # If "output" argument given, write the text to the file
    if args.output != None:
        with open(args.output, 'w') as f:
            f.write(text)



if __name__ == "__main__":
    main()