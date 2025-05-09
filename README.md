# 8mb
8MB video compression bash script for ffmpeg. 

I refuse to pay for Discord Nitro. Stop giving them money. They've raised [$0.9945 Bn of Venture Capital](https://www.crunchbase.com/organization/discord/company_financials). They don't need your money.

## Installation
```bash
curl -s https://raw.githubusercontent.com/matthewbaggett/8mb/main/8mb | sudo tee /usr/local/bin/8mb >/dev/null; sudo chmod +x /usr/local/bin/8mb
```
and now 8mb should be in your PATH:
```bash
8mb -h
```

## What's New
* Removed Docker integration
* Added dependency checks, helping user to install them if not found
* Added comments to install bash script

### But CodingCat, why remove docker?
I felt like it wasn't needed for the relatively small scope of this application. As there is a fork made more for windows already, I figured it'd be better to make this fork Linux only.
This will reduce the work required for running the program (as you don't have to install Docker to do so). To make up for the now lack of automatic dependency fufillment, the script that runs the program now checks to see if python and ffmpeg are installed, and installs them if not.

Currently, Arch based, Debian based, and Red Hat based linux distros are supported.

## Usage
It supports the following flags:
 * --file/-f: The file to compress
 * --size/-s: The target size in MB (so you can stop forking this repo just to change the size...)
 * --tolerance/-t: The tolerance in percentage points

## Example
New, iterative process usage:
```
matthewbaggett@exploding-bolts:~$ 8mb.py -f ~/Downloads/chooch.mp4
Attempt 1 : Transcoding /home/geusebio/Downloads/chooch.mp4 at bitrate 52667
Attempt 1 : Original size: 48.30 MB New size: 3.59 MB Percentage of target: 45 and bitrate 52667
Attempt 2 : Transcoding /home/geusebio/Downloads/chooch.mp4 at bitrate 117441
Attempt 2 : Original size: 48.30 MB New size: 4.80 MB Percentage of target: 60 and bitrate 117441
Attempt 3 : Transcoding /home/geusebio/Downloads/chooch.mp4 at bitrate 195825
Attempt 3 : Original size: 48.30 MB New size: 6.28 MB Percentage of target: 78 and bitrate 195825
Attempt 4 : Transcoding /home/geusebio/Downloads/chooch.mp4 at bitrate 249600
Attempt 4 : Original size: 48.30 MB New size: 7.30 MB Percentage of target: 91 and bitrate 249600
Completed in 4 attempts.
```
Attempt 4 : Transcoding /home/geusebio/Downloads/chooch.mp4 at bitrate 249600
Attempt 4 : Original size: 48.30 MB New size: 7.30 MB Percentage of target: 91 and bitrate 249600
Completed in 4 attempts.
```
