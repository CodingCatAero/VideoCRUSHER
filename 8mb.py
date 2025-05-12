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
parser.add_argument("-s", "--size", help="Target Size in MiB (1024 KiB)", type=int, default=8, required=False)
parser.add_argument("-t", "--tolerance", help="Tolerance in % (default: 5)", type=int, default=5, required=False)
parser.add_argument('-o', '--output', help='Name for output filename (default: <file>.crushed.<file type>)', required=False)
args = parser.parse_args()

# Returns a string which contains the correct size factor for the amount of bytes thrown in
def determineByteSize(bytes, perSecond=0):
    if perSecond == 1:
        byteSize = ["Bit/s", "Kbit/s", "Mbit/s", "Gbit/s", "Tbit/s", "Pbit/s", "Ebit/s", "Zbit/s"]
        numerator = 1000
    else:
        byteSize = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]
        numerator = 1024

    sizeIndex = 0

    while (bytes > numerator):
        sizeIndex += 1
        bytes /= numerator

    return f"{round(bytes, 2)} {byteSize[sizeIndex]}"

# Assigns args to variables
tolerance = args.tolerance
fileInput = args.file

if args.output:
    fileOutput = args.output
else:
    fileOutput = f"{fileInput[:fileInput.rindex('.')]}_CRUSHED_{fileInput[fileInput.rindex('.'):]}"

targetSizeBytes = (args.size * 1024) * 1024

# Should get the duration of the video as a float by running a subprocess, reading the stdout, and turning it into a float
durationSeconds = float((subprocess.run(f"ffprobe -i \"{fileInput}\" -show_entries format=duration -v quiet -of csv=\"p=0\"", 
                  shell=True, text=True, capture_output=True)).stdout)

# Rough calculation of bitrate by dividing target bytes by duration of video
bitrate = targetSizeBytes / durationSeconds

print(f"Crushing {fileInput} to {determineByteSize(targetSizeBytes)} with {tolerance}% tolerance.", end="\n\n")

factor = None
attempt = 0

# Should loop while the video is larger or smaller than the target size +/- the tolerance %
while (factor == None or factor > 1.0 + (tolerance/100.0) or factor < 1.0 - (tolerance/100.0)) and bitrate > 5000:
    attempt += 1

    # Sets the target bitrate by taking the existing bitrate and multiplying it by 1 (On initial loop), or by the factor of size which the video is larger
    bitrate = round(bitrate * (factor or 1))

    if bitrate < 5000:
        print("BITRATE TOO LOW. Setting to 5KiB/s and terminating crushing after this transcode.", end="\n\n")
        bitrate = 5000

    print(f"Attempt {attempt}: Transcoding {fileInput} at {determineByteSize(bitrate, perSecond=1)}")

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

print(f"Completed in {attempt} attempts over {round(time.time() - startTime, 2)} seconds")
print(f"Crushed and exported as {fileOutput}")