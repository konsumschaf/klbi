# Konsumschaf's LaunchBox Importer
Script that imports the LaunchBox export folder into RetroArch consoles.

[LaunchBox](https://www.launchbox-app.com) allows the users to move some (or all) of their ROM collection to an Android device to be used with the Android version of LaunchBox.

This script allows you to import these files to your Linux device running a custom firmware with EmulationStation.

# Supported Firmwares
* [351ELEC](https://351elec.de)

# Limitations
Right now it's only tested with 351ELEC.

# Easy Usage
## On the device
* Connect the device to your Windows PC using SMP (`//351elec`) and chose the `rom` folder
* Place the `klbi.py` and `klbi.sh` scripts in the Ports folder of your device

## On Windows running LaunchBox
* Select the ROMs you want to export (for convenience, you can create a playlist for this)
* Highlight all the ROMs you want to export
* Chose *Tools* -> *Export to Android* -> *Next* -> *Export the selected games only* -> *Next* -> *Next* -> *Next* -> *Copy the files over to Your Device via USB* -> *Browse*
* Select the ROM folder of your device and press *OK*
* *Next*
* Wait for the data to be copied over

## On the device
* Start the `klbi.sh` script in the Ports folder
* Update the Gamelists

# Short usage
Place `klbi.*` in your `/roms/ports/` folder, generate the `LaunchBox` folder with LaunchBox, place it in the ROMs-folder of your device, run the script and refresh the gamelists.

# Details
Logfile will be created on the device in: `/tmp/logs/klbi.log`

# Changelog
2022-01-15: Initial release
