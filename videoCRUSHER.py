#!/usr/bin/python3

# Initializes modules used and starts timer
import subprocess
import os
import argparse
import time
startTime = time.time()

BYTE_SIZES = ["MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]

# Define functions for later use
# Should run an encode with optional video filters
def runEncode(videoInput, videoOutput, overwrite=0):
    subprocess.run(f"ffmpeg -y -i \"{videoInput}\" -hide_banner -loglevel error -c:a libmp3lame -q 30 -compression_level 9 -c:v libx264 -preset ultrafast -crf 30 -vf scale={width}:{height},fps=fps={framerate} \"{videoOutput}\"",
            shell=True, text=True)

    if overwrite == 1:
        subprocess.run(f"cp -f {fileOutput} {fileInput}",shell=True, text=True)

# Should probe the input file for the requested information stream
def runProbe(videoInput, stream):
    return subprocess.run(f"ffprobe -i \"{fileInput}\" -v quiet -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream={stream}", 
        shell=True, text=True, capture_output=True).stdout

# Should return the size of the file in the provided path in MiB
def getVideoSizeMiB(path):
    return os.path.getsize(path)/1024/1024

# Returns a string which contains the correct size factor for the amount of bytes thrown in
def determineCategory(inputValue, categories, numerator):   
    categoryIndex = 0

    while (inputValue > numerator):
        categoryIndex += 1
        inputValue /= numerator

    return f"{round(inputValue, 2)} {categories[categoryIndex]}"

# Parses args from cli command
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='File to crush', required=True)
parser.add_argument("-s", "--size", help="Target Size in MiB (1024 KiB)", type=int, default=8, required=False)
parser.add_argument("-t", "--tolerance", help="Tolerance in % (default: 5)", type=int, default=5, required=False)
parser.add_argument('-o', '--output', help='Name for output filename (default: <file>.crushed.<file type>)', required=False)
args = parser.parse_args()

# Assigns args to variables
fileInput = args.file
targetSizeMiB = args.size

if args.output:
    fileOutput = args.output
else:
    fileOutput = f"{fileInput[:fileInput.rindex('.')]}_CRUSHED.mp4"

framerate = round(int(runProbe(fileInput, "r_frame_rate")[:-3]))

resolution = runProbe(fileInput, "width,height").split()
width = int(resolution[0])
height = int(resolution[1])

tempFileInput = os.path.expanduser('~') + f"/temp{fileInput[fileInput.rindex('/') + 1:]}"

# Initial encode to set baseline and set input to new baseline
runEncode(fileInput, tempFileInput)
fileInput = tempFileInput

print(f"\nCrushing {fileInput[fileInput.rindex('/') + 1:]} to {determineCategory(targetSizeMiB, BYTE_SIZES, 1024)}")

attempt = 0
result = 0
answer = ""

while result == 0 and attempt < 10:
    attempt += 1

    width = round(width*0.80)
    height = round(height*0.80)

    if width % 2 == 1:
        width += 1

    if height % 2 == 1:
        height += 1

    print(f"\nAttempt {attempt}: {width}x{height} @ {framerate}fps")
    runEncode(fileInput, fileOutput, 1)

    if attempt == 6:
        answer = input("\nSafe resolution unable to be found. Would you like to crush to the (l)owest safe resolution, or try (o)bliteration? [l/o/EXIT]: ")

    if getVideoSizeMiB(fileOutput) < targetSizeMiB * (1 + args.tolerance/100) or answer == "l" or answer == "L":
        result = 1
    
    elif answer == "o" or answer == "O":
        framerate = round(framerate*0.80)

    elif attempt >= 6:
        attempt = 11

if result:
    print(f"\nCompleted in {attempt} attempts over {determineCategory(round(time.time() - startTime), ["seconds", "minutes", "hours"], 60)}")
    print(f"Exported as {fileOutput}. Size: {determineCategory(getVideoSizeMiB(fileOutput), BYTE_SIZES, 1024)}")
else:
    print("\nThe video was too strong.. It couldn't be crushed")

subprocess.run(f"rm -f {fileInput}", shell=True, text=True)
print("\nExiting")