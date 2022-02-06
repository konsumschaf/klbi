#!/usr/bin/env python3
#
# Konsumschaf's LaunchBox Importer
#

from dataclasses import dataclass
import os
import pathlib
import shutil
import xml.etree.ElementTree as ET

# Config for the different target systems
# needs path to the ROMs-Folder and the folder names
config = {
    '351elec' : {
        'rom_path' : '/roms',
        'log_path' : '/tmp/logs',
        'log_file' : 'klib.log',
        '3DO Interactive Multiplayer' : '3do',
        'Amstrad CPC' : 'amstradcpc',
        'Arcade' : 'arcade',
        'Atari 2600' : 'atari2600',
        'Atari 5200' : 'atari5200',
        'Atari 7800' : 'atari7800',
        'Atari 800' : 'atari800',
        'Atari Lynx' : 'atarilynx',
        'Atari ST' : 'atarist',
        'ColecoVision' : 'coleco',
        'Commodore 128' : 'c128',
        'Commodore 64' : 'c64',
        'Commodore Amiga CD32' : 'amigacd32',
        'Commodore Amiga' : 'amiga',
        'Commodore Plus 4' : 'c16',
        'Commodore VIC-20' : 'vic20',
        'Fairchild Channel F' : 'channelf',
        'FB-Neo' : 'fbneo',
        'FBNeo' : 'fbneo',
        'GCE Vectrex' : 'vectrex',
        'Magnavox Odyssey 2' : 'odyssey',
        'Mame' : 'mame',
        'MAME' : 'mame',
        'Mattel Intellivision' : 'intellivision',
        'Mega Duck' : 'megaduck',
        'Microsoft MSX' : 'msx',
        'Microsoft MSX2' : 'msx2',
        'MS-DOS' : 'pc',
        'NEC PC-8801' : 'pc88',
        'NEC PC-9801' : 'pc98',
        'NEC PC-FX' : 'pcfx',
        'NEC TurboGrafx-16' : 'tg16',
        'NEC TurboGrafx-CD' : 'tg16cd',
        'Nintendo 64' : 'n64',
        'Nintendo DS' : 'nds',
        'Nintendo Entertainment System' : 'nes',
        'Nintendo Famicom Disk System' : 'fds',
        'Nintendo Game & Watch' : 'gameandwatch',
        'Nintendo Game Boy Advance' : 'gba',
        'Nintendo Game Boy Color' : 'gbc',
        'Nintendo Game Boy' : 'gb',
        'Nintendo Pokemon Mini' : 'pokemini',
        'Nintendo Satellaview' : 'satellaview',
        'Nintendo Virtual Boy' : 'virtualboy',
        'OpenBOR' : 'openbor',
        'PC Engine CD' : 'pcenginecd',
        'PC Engine SuperGrafx' : 'pcengine',
        'Philips Videopac+' : 'videopac',
        'Sammy Atomiswave' : 'atomiswave',
        'ScummVM' : 'scummvm',
        'Sega 32X' : 'sega32x',
        'Sega CD' : 'segacd',
        'Sega Dreamcast' : 'dreamcast',
        'Sega Game Gear' : 'gamegear',
        'Sega Genesis' : 'genesis',
        'Sega Master System' : 'mastersystem',
        'Sega Mega CD 32X' : 'megacd',
        'Sega MegaDrive' : 'megadrive',
        'Sega Naomi' : 'naomi',
        'Sega Saturn' : 'saturn',
        'Sega SC-3000' : 'sc-3000',
        'Sega SG-1000' : 'sg-1000',
        'Sharp X1' : 'x1',
        'Sharp X68000' : 'x68000',
        'Sinclair ZX Spectrum' : 'zxspectrum',
        'Sinclair ZX-81' : 'zx81',
        'SNK Neo Geo CD' : 'neocd',
        'SNK Neo Geo MVS' : 'neogeo',
        'SNK Neo Geo Pocket Color' : 'ngpc',
        'SNK Neo Geo Pocket' : 'ngp',
        'Sony Playstation' : 'psx',
        'Sony PSP Minis' : 'pspminis',
        'Sony PSP' : 'psp',
        'Super Famicom' : 'famicom',
        'Super Nintendo Entertainment System' : 'snes',
        'Watara Supervision' : 'supervision',
        'WonderSwan Color' : 'wonderswancolor',
        'WonderSwan' : 'wonderswan',
    },
}
config["debug"] = config["351elec"].copy()
config["debug"].update({
    'rom_path' : '/tmp/klbi',
    'log_path' : '/tmp/klbi/logs',
    })

metadata_dict = {
    'Title' : 'name',
    'Notes' : 'desc',
    'Favorite' : 'favorite',
    'Developer' : 'developer',
    'Publisher' : 'publisher',
    'Genre' : 'genre',
    'PlayCount' : 'playcount',
    'PlayTime' : 'gametime',
}

# Guess the device we are running on
def get_os():
    # set "debug" as default
    current_os = "debug"
    # 351elec
    os_config_file = '/etc/os-release'
    if os.path.isfile(os_config_file):
        with open(os_config_file, encoding="utf-8") as f:
            name = f.readline().strip()
            if name == 'NAME="351ELEC"':
                current_os = "351elec"

    return current_os

# Logging
@dataclass
class Logger:
    dir: str
    file: str

    script_basename = os.path.basename(__file__)

    def __post_init__(self):
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        self.file_handle = open(f'{self.dir}/{self.file}',"w")

    def log(self, text: str) -> None:
        print(f'{self.script_basename}: {text}')
        self.file_handle.write(f'{self.script_basename}: {text}\n')

    def __del__(self):
        self.file_handle.close()



# Python 3.8 does not know about prettyprint xml, so this is a workaround:
def indent(elem, level=0):
    i = os.linesep + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



# Set the correct OS
current_os = get_os()
os_config = config[current_os]

# Open the logfile
logger = Logger(dir = os_config['log_path'], file = os_config['log_file'])

logger.log(f'OS: {current_os}')

if not os.path.exists(f'{os_config["rom_path"]}/LaunchBox'):
    logger.log("No LaunchBox folder found, aborting")
    exit(1)

# Get all the systems
lb_xml_files = os.listdir(f'{os_config["rom_path"]}/LaunchBox/Data/Platforms/')

for lb_xml_file in lb_xml_files:
    writefile = False
    if pathlib.Path(lb_xml_file).suffix == '.xml':
        # open LaunchBox xml file
        lb_tree = ET.parse(f'{os_config["rom_path"]}/LaunchBox/Data/Platforms/{lb_xml_file}')
        lb_root = lb_tree.getroot()

        system = lb_root.find("./Platform/Name").text
        logger.log(f'Processing system: "{system}"')

        # Check if system is known
        if system not in os_config:
            logger.log(f'  Unknown system "{system}", trying Scrap-As-Fallback')
            scrape_as = lb_root.find("./Platform/ScrapeAs").text
            if scrape_as not in os_config:
                logger.log(f'  Scrape-As-System: "{scrape_as}" not found, skipping')
                continue
            else:
                system = scrape_as
                logger.log(f'  Known Scrape-As-System: "{scrape_as}" found, use it as system')

        # Open systems gamelist.xml or create one if missing
        gamelist_path = f'{os_config["rom_path"]}/{os_config[system]}/gamelist.xml'
        if os.path.exists(gamelist_path):
            es_tree = ET.parse(gamelist_path)
            es_root = es_tree.getroot()
        else:
            es_root = ET.Element('gameList')
            es_tree = ET.ElementTree(element = es_root)

        # Generate list of all games in gamelist.xml
        exisiting_games_list = []
        if es_root.find('game'):
            for existing_game in es_root.findall('game/path'):
                exisiting_games_list.append(existing_game.text)

        for games in lb_root.findall('Game'):
            rom_source_path = games.find("ApplicationPath").text
            rom_name = os.path.basename(rom_source_path)
            rom_stem = pathlib.Path(rom_name).stem
            rom_source_full_path = f'{os_config["rom_path"]}/LaunchBox/{rom_source_path}'

            # Check if this ROM is already on the system
            rom_full_target_path = f'{os_config["rom_path"]}/{os_config[system]}/{rom_name}'
            if not os.path.exists(rom_full_target_path):
                # Check if the source file exists
                if os.path.exists(rom_source_full_path):
                    # Move the ROM over to the correct folder
                    logger.log(f'  Adding new game "{rom_name}"')
                    # if the rom folder does not exist, create it
                    os.makedirs(os.path.dirname(rom_full_target_path), exist_ok=True)
                    shutil.move(rom_source_full_path, rom_full_target_path)

                    # Check if this ROM is already in the gamelist.xml
                    if f'./{rom_name}' not in exisiting_games_list:
                        writefile = True

                        # Add new Game to xml
                        newGame = ET.SubElement(es_root, "game")

                        # Convert Standard Metadata
                        for source in metadata_dict:
                            ET.SubElement(newGame, metadata_dict[source]).text = games.find(source).text

                        # Add the Game to the gamelist.xml
                        ET.SubElement(newGame, "path").text = f'./{rom_name}'

                        # Add the images
                        image_dict = {
                            'AndroidBoxFrontFullPath' : {'target_xml' : 'image', 'target_suffix' : 'image'},
                            'AndroidBoxFrontThumbPath' : {'target_xml' : 'thumbnail', 'target_suffix' : 'thumb'},
                            'AndroidBackgroundPath' : {'target_xml' : 'boxback', 'target_suffix' : 'boxback'},
                            'AndroidGameTitleScreenshotPath' : {'target_xml' : 'titleshot', 'target_suffix' : 'titleshot'},
                            'AndroidClearLogoFullPath' : {'target_xml' : 'marquee', 'target_suffix' : 'marquee'}
                        }
                        for source_xml in image_dict:
                            if (image_file := games.find(source_xml)) is not None:
                                image_file = image_file.text
                                image_extension = pathlib.Path(image_file).suffix
                                short_image_path = f'images/{rom_stem}-{image_dict[source_xml]["target_suffix"]}{image_extension}'
                                image_source = f'{os_config["rom_path"]}/LaunchBox/{image_file}'
                                image_target = f'{os_config["rom_path"]}/{os_config[system]}/{short_image_path}'
                                # if the image folder does not exist, create it
                                os.makedirs(os.path.dirname(image_target), exist_ok=True)
                                if os.path.exists(image_source):
                                    shutil.move(image_source, image_target)
                                    ET.SubElement(newGame, image_dict[source_xml]["target_xml"]).text = f'./{short_image_path}'
                                else:
                                    logger.log(f'  Skipping image "{image_file}" file "{image_source}" does not exist')

                        # Add the video
                        if (video_file := games.find("AndroidGameplayScreenshotPath")) is not None:
                            video_file = video_file.text
                            # Really a video?
                            if pathlib.PurePath(video_file).parts[0] == 'Videos':
                                video_extension = pathlib.Path(video_file).suffix
                                short_video_path = f'videos/{rom_stem}-video{video_extension}'
                                video_source = f'{os_config["rom_path"]}/LaunchBox/{video_file}'
                                video_target = f'{os_config["rom_path"]}/{os_config[system]}/{short_video_path}'
                                # if the video folder does not exist, create it
                                os.makedirs(os.path.dirname(video_target), exist_ok=True)
                                if os.path.exists(video_source):
                                    shutil.move(video_source, video_target)
                                    ET.SubElement(newGame, "video").text = f'./{short_video_path}'
                                else:
                                    logger.log(f'  Skipping image "{video_file}" file "{video_source}" does not exist')
                    else:
                        logger.log(f'  Skipping "{rom_name}" entry, already in gamelist.xml')
                else:
                    logger.log(f'  Skipping "{rom_name}" source file "{rom_source_full_path}" does not exist')
            else:
                logger.log(f'  Skipping "{rom_name}", game already exits')

        if writefile:
            logger.log("  Writing new gamelist.xml")
            # Format the xml output nicely
            # not in python3.8 :-(
            # ET.indent(es_root, space="\t", level=0)
            # Workaround:
            indent(es_root)
            es_tree.write(gamelist_path)
            #print(ET.tostring(es_root))
            #print()

# Cleaning up
logger.log("Removing LaunchBox folder")
shutil.rmtree(f'{os_config["rom_path"]}/LaunchBox')