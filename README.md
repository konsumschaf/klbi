# Konsumschaf's LaunchBox Importer
Script that imports the LaunchBox export folder into RetroArch consoles.

[LaunchBox](https://www.launchbox-app.com) allows the users to move some (or all) of their ROM collection to an Android device to be used with the Android version of LaunchBox.

This script allows you to import these files to your Linux device running a custom firmware with EmulationStation.

# Supported Firmwares
* [AmberELEC](https://amberelec.org) (formerly known as 351elec)

# Limitations
* Right now it's only tested with AmberELEC.
* If the ROM is missing on the device, but there are already some entrys in the gamelist.xml, only the ROM wil be moved. But the images and videos will not (hard to tell, what to do with the orphaned entry). You can clean up the old gamelist.xml first by entering Emulationstation *Main Menu* -> *System Settings* -> *Developer* -> **Clean Gamelists & Remove unused Media**.

# Easy Usage
## On the device
* Connect the device to your Windows PC using SMP (`//AmberELEC`) and choose the `rom` folder
* Place the `klbi.py` and `klbi.sh` scripts in the Ports folder of your device

## On Windows running LaunchBox
* Select the ROMs you want to export (for convenience, you can create a playlist for this). You can choose ROMs for multiple systems at once if you like.
* Highlight all the ROMs you want to export
* Chose
  * *Tools*
  * *Export to Android*
  * *Next*
  * *Export the selected games only*
  * *Next*
  * *Next*
  * *Next*
  * *Copy the files over to Your Device via USB* (Yes, *USB-Export* is correct, this will bring up a general file-browser)
  * *Browse*
  * Select the ROM folder of your device and press *OK*
  * *Next*
* Wait for the data to be copied over

## On the device
* Start *klbi* in the *Ports* Section
* Update the Gamelists in the Emulationstation menu

# Short usage
Place `klbi.*` in your `/roms/ports/` folder, generate the `LaunchBox` folder with LaunchBox, place it in the ROMs-folder of your device, run the script and refresh the gamelists.

# Details
Logfile will be created on the device in: `/tmp/logs/klbi.log`

# Changelog
**2022-04-03**: Add Support for LastPlayedDate and changed 351elec to AmberELEC, clean-up code

**2022-02-09**: Clean-up code

**2022-02-08**: Convert more metadata (rating, number of players and release date)

**2022-02-05**: Add Scrap-As-Fallback if system is unknown, clean-up

**2022-01-23**: Add video-support, add logging to stdout, bug-fixing

**2022-01-15**: Initial release
