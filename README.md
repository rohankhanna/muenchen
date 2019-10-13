# muenchen
Useful tools for newcomers in Munich

## [blauekarte.py](blauekarte.py)
Recently it became hard to get an appointment for Blue Card EU in Munich.
This script is intended for monitoring available appointments. Optionally, you
can implement your own alarm function (e.g. send an SMS to mobile phone). By
default, the script checks for available appointments every 120 seconds,
assuming that you need an appointment for a single person. This could be changed
by passing different values to the TerminChecker class constructor (see class
declaration).

The script doesn't book an appointment, but only reports the availability.
You should book the appointment manually on the [immigration office page
](https://www.muenchen.de/rathaus/terminvereinbarung_abh.html?cts=1080627).
