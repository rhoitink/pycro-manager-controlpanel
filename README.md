# pycro-manager-controlpanel

Software to use an old Leica SP2 control panel to control micro-manager settings (via pycro-manager).

## Background info
Recently a new confocal operated by [µManager](https://micro-manager.org/) was installed in our group. It's a nice feature to alter e.g. laser powers via a physical button/knob. We were looking for a cheap option to do so with materials we had lying around.

One of the pieces of hardware that we had lying around was a Leica SP2/NT control panel, which seemed suitable for this project. The control panel was connected to the old PC using two cables: an RS232 serial port and a [game port](https://en.wikipedia.org/wiki/Game_port). It turned out that we could power the panel using 12 V DC over the game port cable and then use the serial port for communication with the PC.

Using a serial-to-USB connector, the panel was connected to the microscope PC and by analysing the signals that it transmitted, we figured out the following;
Every time a knob is turned, the panel sends a single byte over serial, an 8 bits long signal with the following information, that it built up as follows (`0b` is the python binary prefix):

```
0b12345678

bits 1-3 : always 1
bits 4-6 : indicate the button: 001 for the rightmost untill 111 for the leftmost one
bit 7    : 1 for clockwise, 0 for counter-clockwise
bit 8    : always 1
```

The output on the serial port is continuously read and parsed by [parser.py](./pycontrolpanel/parser.py), that converts it an instance of the `Button` helper class (see [signals.py](./pycontrolpanel/signals.py)), which basically is a wrapper with a button number and a direction.
[gui.py](./pycontrolpanel/gui.py) is where most logic occurs. It presents the user with a simple GUI to connect to µManager and the serial port and then reads out the data, parses it and sends it back to µManager core.

## Known issue
Even though the response of µManager core is very fast, the GUI itself does not automatically update. To see the updated laser powers also in the GUI, the user needs to manually press the `Refresh` button for it to update.

## Installation

### Requirements
* Python 3.8+
* Micro-Manager 2.0.0 (other versions might work, but need a different version of [pycromanager](https://github.com/micro-manager/pycro-manager))


Preferably create a virtual environment to avoid package conflicts. See [for example here](https://docs.python.org/3/library/venv.html) on how to do so.
Installation via `pip` using:

Run:
```sh
python -m pip install git+https://github.com/rhoitink/pycro-manager-controlpanel
```

## Starting the software

After installation, the software can be started via the `pycontrolpanel` command. There are some command line arguments that can be used to set for example the serial port or baud rate. All arguments can be viewed by running `pycontrolpanel --help`