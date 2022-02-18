#!/bin/python3

import sys
import argparse
import audio_from_file
import audio_from_mic


def main():
    parser = argparse.ArgumentParser(
        description="Script to convert speech to text", conflict_handler="resolve")
    inp = parser.add_mutually_exclusive_group(required=False)
    inp.add_argument(
        "-i", "--input-file", help='Input from file (\'-\' To read file name from stdin)', action="store",dest = "input_file")
    inp.add_argument(
        "-m", "--mic", help='Input from microphone', action="store_true")

    parser.add_argument(
        '-o', '--output', help='Output file (\'-\' To output into stdout)', required=False, metavar="")
    parser.add_argument(
        '-f', '--offline', help='Offline mode', required=False, action='store_true')

    args = parser.parse_args()

    if args.input_file == '-':
        input_file = sys.stdin.readline().strip()
    else:
        input_file = args.input_file

    is_quite = False if args.output == '-' or args.output == None else True

    if args.mic or (args.input_file == None):
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
