# talk-a-box
rp2040 based talking toy

[UNFORTUNATELY VIBECODED]

## How does this thing work
This project runs on a rp2040 Pi Pico clone with 16MB of flash memory. There are 41 audio files in wav format (that I can't distribute) saved to the flash storage of the device. After a press of a pushbutton, the device randomly takes one of the files and plays it on the speaker, then goes to sleep, until the button is pressed again. There is a playlist functionality built in with shuffle applied, so it's not truly random.
## What do you need to build this
- Rpi2040 pi pico clone with larger flash (I used 16MB one)
- 8 ohm speaker
- LiPo battery and charging module
- push button and power switch
- MAX98357A amplifier

### Notes on audio files
- if you use your own audio files, change the count of the files on line 24.
- the file naming scheme should be as follows: 0001.wav, 0002.wav, 0003.wav etc.
- the files should be stored in /audio/ folder

## Wiring
- LiPo module to VBUS
- PI GP0 to amp BCLK
- PI GP1 to amp LRCLK
- PI GP2 to amp DIN
- Pi GP6 to amp SD
- pushbutton to PI GP3
- make sure to properly ground everything (charging module, the other button lead, speaker and the AMP)