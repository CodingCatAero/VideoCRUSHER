# VideoCRUSHER
Video CRUSHING python script (with BASH integration) for ffmpeg. 

I also refuse to pay for Discord Nitro. Stop giving them money. They've raised [$0.9945 Bn of Venture Capital](https://www.crunchbase.com/organization/discord/company_financials). They don't need your money.

## Installation on GNU/Linux based OSes
Download ``installVideoCRUSHER`` and in it's directory run:
```bash
bash installVideoCRUSHER
```

## Installation on other OSes
I don't have a windows PC or Mac, so unfortunatelly I'm unfamiliar with how to set up powershell/terminal integration on those machines.

You're more than free to form this project and give it a shot yourself! I highly recommend doing that with a simple project like this to help learn git.

In the meantime, you can just download `` videoCRUSHER.py `` and run it through CLI using `` python ``.

## Updating
Just run `` bash installVideoCRUSHER `` again.

## Uninstallation
Download ``uninstallVideoCRUSHER`` and in it's directory run:
```bash
bash uninstallVideoCRUSHER
```

## What's New
* Added lower bound for bitrate to stop crashing
* Added seperate install script
* Added accurate percentage calculation
* Bitrate and size now show proper factors
* Added comments for everything now
* re-implimented abandoned output flag
* Updated MB/KB to Mib/Kib becuase that's the math being used
* Cleaned up output

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
 * --size/-s: The target size in MiB
 * --tolerance/-t: The tolerance in percentage points
 * --output/ -o: The name of the output file

## Example
New, cleaned up output:
```
Crushing /home/PapercrownKitty/Downloads/test.mp4 to 10.0 MiB with 5% tolerance.

Attempt 1: Transcoding /home/PapercrownKitty/Downloads/test.mp4 at 321.47 Kbit/s
Result: Original size: 11.36 MiB. New size: 1.64 MiB. Percentage of target: 16%. Bitrate: 321.47 Kbit/s

Attempt 2: Transcoding /home/PapercrownKitty/Downloads/test.mp4 at 1.96 Mbit/s
Result: Original size: 11.36 MiB. New size: 7.87 MiB. Percentage of target: 79%. Bitrate: 1.96 Mbit/s

Attempt 3: Transcoding /home/PapercrownKitty/Downloads/test.mp4 at 2.49 Mbit/s
Result: Original size: 11.36 MiB. New size: 9.87 MiB. Percentage of target: 99%. Bitrate: 2.49 Mbit/s

Completed in 3 attempts over 14.11 seconds
Crushed and exported as /home/PapercrownKitty/Downloads/test.crushed.mp4
```