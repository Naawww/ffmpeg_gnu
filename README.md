# AAREF GNU Radio project
## Hardware
I've installed the **Noolectric NESDR Smartee** dongle. It's come out as:
- Generic RTL2832U OEM :: 00000001

I've confirmed this works in **CubicSDR**.

It seems this dongle I've got uses the ubiqutous RTL2832U chip - which is an RTL-SDR chip. 

The documentation of the RTL-SDR source block states that they support this chip through this module:
- librtlsdr

### Osmocom wiki
https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr

#### testing the device
I got the drivers again, and some testing files from here:
https://inst.eecs.berkeley.edu/~ee123/sp15/rtl_sdr_install.html

I've moved these to the rtlsdr_win directory in this project. 
Ok, so I eventually got the rtl_test.exe to run, by specifying device 1:

`rtl_test.exe -d 1`

**I think I'm going to have to specify device one generally.**

#### using rtl-sdr
The rtl-sdr.exe behaves much like ffmpeg. you call it `rtl_sdr.exe -d 1` and
after indicating it has successfully connected to the device, it spits out 
loads of options for how you want your signal taking in etc.

So, I think that in GNU Radio Companion, we can use this as the entry point.

#### Hooking up to GNU radio companion
Seems instead, you need to use the serial number.
So, for mine, in the "device arguments" of the osmocom source:
`rtl=00000001`

## Software
I've got ffmpeg

I've also got the ffmpeg-python module, which seems to work as I was able 
to use it to extract frames from a video alex sent me.

I've also got GNU Radio Companion. Python blocks can be made and they expect set
inputs and outputs. but internally, they seems to be quite easy about how
this data is handled.

First, need to get some input. Could simply use a sine wave initially. 
Then need to feed this into FFMPEG and convert it to a suitable format.

## Examples:
http://www.stargazing.net/david/GNUradio/RTLFMstations.html
