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

# If an output has been assigned, use that. Else, auto-generate one
if args.output:
    fileOutput = args.output
else:
    fileOutput = f"{fileInput[:fileInput.rindex('.')]}_CRUSHED.mp4"

# Should grab the framerate of the input video
framerate = round(int(runProbe(fileInput, "r_frame_rate")[:-3]))

# Should grab the resolution of the input video
resolution = runProbe(fileInput, "width,height").split()
width = int(resolution[0])
height = int(resolution[1])

# Should make a tempFile path in the user's HOME directory
tempFileInput = os.path.expanduser('~') + f"/temp{fileInput[fileInput.rindex('/') + 1:]}"

# Initial encode to set baseline and set input to new baseline
runEncode(fileInput, tempFileInput)
fileInput = tempFileInput

print(f"\nCrushing {fileInput[fileInput.rindex('/') + 1:]} to {determineCategory(targetSizeMiB, BYTE_SIZES, 1024)}")

attempt = 0
result = 0
answer = ""

# Should loop until 10 atttempts have been made, the crushing succeeds, or the user wishes to quit at the 6th attempt
while result == 0 and attempt < 10:
    attempt += 1

    # Reduces the resolution by %20
    width = round(width*0.80)
    height = round(height*0.80)

    if width % 2 == 1:
        width += 1

    if height % 2 == 1:
        height += 1

    print(f"\nAttempt {attempt}: {width}x{height} @ {framerate}fps")
    runEncode(fileInput, fileOutput, 1)

    # Once the 6th attempt is reached, ask if the user wishes to quit, keep going, or crush to the lowest safe resolution
    if attempt == 5:
        answer = input("\nSafe resolution unable to be found. Would you like to crush to the (l)owest safe resolution, or try (o)bliteration? [l/o/EXIT]: ")

    # If the user chooses to crush to the lowest safe res, or the output file size is below threshold, should set result to 1
    if os.path.getsize(fileOutput)/1024/1024 < targetSizeMiB * (1 + args.tolerance/100) or answer == "l" or answer == "L":
        result = 1
    
    # If the user has chosen to keep going, begin also reducing fps
    elif answer == "o" or answer == "O":
        framerate = round(framerate*0.80)

    # If the user hasn't chosen either option when asked, delete outputFile and quit
    elif attempt >= 6:
        subprocess.run(f"rm -f {fileOutput}", shell=True, text=True)
        attempt = 11

if result:
    print(f"\nCompleted in {attempt} attempts over {determineCategory(round(time.time() - startTime), ["seconds", "minutes", "hours"], 60)}")
    print(f"Exported as {fileOutput}. Size: {determineCategory(os.path.getsize(fileOutput)/1024/1024, BYTE_SIZES, 1024)}")
else:
    print("\nThe video was too strong.. It couldn't be crushed")

# Should delete tempFile
subprocess.run(f"rm -f {fileInput}", shell=True, text=True)
print("\nExiting")