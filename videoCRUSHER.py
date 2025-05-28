#!/usr/bin/python3

# Initializes modules used and starts timer
import sys
import subprocess
import os
import argparse
import time
startTime = time.time()

# Parses args from cli command
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='File to crush', required=True)
parser.add_argument("-s", "--size", help="Target Size in MB (1000 KB)", type=int, default=8, required=False)
parser.add_argument("-t", "--tolerance", help="Tolerance in % (default: 5)", type=int, default=5, required=False)
parser.add_argument('-o', '--output', help='Name for output filename (default: <file>.crushed.<file type>)', required=False)
args = parser.parse_args()

RESOLUTIONCRUSH={0.35, 0.55, 0.67, 0.74, 0.78}

# Assigns args to variables
tolerance = args.tolerance
fileInput = args.file

if args.output:
    fileOutput = args.output
else:
    fileOutput = f"{fileInput[:fileInput.rindex('.')]}_CRUSHED{fileInput[fileInput.rindex('.'):]}"

fileOutputName = f"{fileOutput[fileInput.rindex('/') + 1:]}"

newFileInput = os.path.expanduser('~') + f"/temp{fileOutputName}"

targetSizeBytes = args.size * 1000 * 1000


# Initial encode to set baseline
subprocess.run(f"ffmpeg -y -i \"{fileInput}\" -hide_banner -loglevel error -c:v libx264 -preset slow -crf 30 -c:a copy \"{newFileInput}\"",
            shell=True, text=True)

# Should get the duration of the new baseline by running a subprocess, reading the stdout, and turning it into a float
videoSize = int(subprocess.run(f"ffprobe -v error -select_streams v -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \"{newFileInput}\" | awk \'{{totalSize+=$1}} END {{print totalSize}}\'", 
    shell=True, text=True, capture_output=True).stdout)

durationSeconds = float(subprocess.run(f"ffprobe -i \"{newFileInput}\" -show_entries format=duration -v quiet -of csv=\"p=0\"", 
    shell=True, text=True, capture_output=True).stdout)

resolution = subprocess.run(f"ffprobe -v error -select_streams v:0 -show_entries stream=height,width -of default=nokey=1:noprint_wrappers=1 \"{newFileInput}\"", 
    shell=True, text=True, capture_output=True).stdout.split()

def crushByBitrate(tolerance, bitrate, targetSizeBytes, fileInput, fileOutput):
    factor = None

    while (factor == None or (factor > 1.0 + (tolerance/100.0) or factor < 1.0 - (tolerance/100.0)) and bitrate > 1000):
        attempt+=1

        # Sets the target bitrate by taking the existing bitrate and multiplying it by 1 (On initial loop), or by the factor of size which the video is larger
        bitrate = round(bitrate * (factor or 1))

        if bitrate < 1000:
            print("Bitrate reached lower bound. Terminating..", end="\n\n")
            bitrate = 1000

        else:
            print(f"Transcoding {fileInput} at {determineByteSize(bitrate, perSecond=1)}")

            # Transcodes using the above function   
            subprocess.run(f"ffmpeg -y -hide_banner -loglevel error -i \"{fileInput}\" -b:v {str(bitrate)} -cpu-used {str(os.cpu_count())} -c:a copy \"{fileOutput}\"",
            shell=True, text=True)

            # Gets before and after sizes
            beforeSizeBytes = os.stat(fileInput).st_size
            afterSizeBytes = os.stat(fileOutput).st_size

            # Determines the percentage that the transcoded filesize is in reference to the target size 
            # (e.g. 50% means the transcoded file size is half of the target)

            # The factor is how much to multiply or devide the bitrate by to get closer to the targer 
            # (e.g. If the transcoded file is 150% of the target, the factor is 100/150 = 0.75)
            percentOfTarget = (afterSizeBytes/targetSizeBytes) * 100.0
            factor = 100.0/percentOfTarget

            print(f"Result: Original size: {determineByteSize(beforeSizeBytes)}. New size: {determineByteSize(afterSizeBytes)}. Percentage of target: {round(percentOfTarget)}%. Bitrate: {determineByteSize(bitrate, perSecond=1)}", end="\n\n")

# Returns a string which contains the correct size factor for the amount of bytes thrown in
def determineByteSize(bytes, perSecond=0):
    if perSecond == 1:
        byteSize = ["Bit/s", "Kbit/s", "Mbit/s", "Gbit/s", "Tbit/s", "Pbit/s", "Ebit/s", "Zbit/s"]

    else:
        byteSize = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]

    sizeIndex = 0

    while (bytes > 1000):
        sizeIndex += 1
        bytes /= 1000

    return f"{round(bytes, 2)} {byteSize[sizeIndex]}"



print(f"Crushing {fileInput} to {determineByteSize(targetSizeBytes)} with {tolerance}% tolerance.", end="\n\n")

# # Should loop while the video is larger or smaller than the target size +/- the tolerance %
attempt = 0

widthResolution = int(resolution[0])
heightResolution = int(resolution[1])

for percentageDecrease in RESOLUTIONCRUSH:
    attempt+=1
    print(f"\nAttempt {attempt}. Resolution: {widthResolution}x{heightResolution}")

    widthResolution *= 0.75
    heightResolution *= 0.75

    widthResolution = round(widthResolution)
    heightResolution = round(heightResolution)

    if widthResolution % 2 == 1:
        widthResolution += 1

    if heightResolution % 2 == 1:
        heightResolution += 1

    if (videoSize)*(1-percentageDecrease) < targetSizeBytes:

        print("Resolution to crush to found. Crushing now..")
        subprocess.run(f"ffmpeg -y -i \"{fileInput}\" -hide_banner -loglevel error -c:v libx264 -preset slow -crf 30 -vf scale={widthResolution}:{heightResolution} -c:a copy \"{fileOutput}\"",
            shell=True, text=True)

answer = input("\nWould you like to crush to the (l)owest resolution, or try (o)bliteration? [l/o/EXIT]: ")

if answer == "l" or answer == "L":
    print("\nCrushing now..")
    subprocess.run(f"ffmpeg -y -i \"{fileInput}\" -hide_banner -loglevel error -c:v libx264 -preset slow -crf 30 -vf scale={widthResolution}:{heightResolution} -c:a copy \"{newFileInput}\"",
    shell=True, text=True)

    result = 1

elif answer == "o" or answer == "O":

    answer = input("\nAre you sure you want to OBLITERATE it? THIS WILL MAKE IT UNWATCHABLE. Continue? [y/N]: ")

    if answer == "y" or answer == "Y":
        subprocess.run(f"ffmpeg -y -i \"{fileInput}\" -hide_banner -loglevel error -c:v libx264 -preset slow -crf 30 -vf scale={widthResolution}:{heightResolution} -c:a copy \"{newFileInput}\"",
            shell=True, text=True)

        # Get the crushed video's size
        videoSize = int(subprocess.run(f"ffprobe -v error -select_streams v -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \"{newFileInput}\" | awk \'{{totalSize+=$1}} END {{print totalSize}}\'", 
            shell=True, text=True, capture_output=True).stdout)

        # Rough calculation of bitrate by dividing target bytes by duration of video
        bitrate = round(videoSize / durationSeconds)
        targetBitrate = round(targetSizeBytes / durationSeconds)

        crushByBitrate(tolerance, bitrate, targetSizeBytes, newFileInput, fileOutput)

        print(f"\nCompleted in {attempt} attempts over {round(time.time() - startTime, 2)} seconds")
        print(f"Crushed and exported as {fileOutput}")

subprocess.run(f"rm -f {newFileInput}", shell=True, text=True)
print("\nExiting")