import os
import re
import xml.etree.ElementTree as ET
from rapidfuzz import fuzz
from tracker.models import Game, GameVersion, Platform
from datetime import datetime

# Missing consoles from scrape:
# Amstrad PCW
# Atari 400
#
# Missing consoles from IGDB:
# Atari 400 + 800 (calls them Atari 8-bit)
#
# Skipped scraped or (IGDB) consoles:
# arcade (Arcade): umbrella for any arcade machine, it seems. Want more specificity
#
# 
# Dict below maps ES-DE's folder names with IGDB's platform names
SCRAPED_PLATFORM_DICT = {
    '/3do/': '3DO Interactive Multiplayer',
    '/adam/': 'Adam', # No IGDB
    '/ags/': 'PC',
    '/amiga/': 'Amiga',
    '/amiga600/': 'Amiga 600', # No IGDB
    '/amiga1200/': 'Amiga 1200', # No IGDB
    '/amigacd32/': 'Amiga CD32',
    '/amstradcpc/': 'Amstrad CPC',
    '/android/': 'Android',
    '/apple2/': 'Apple II',
    '/apple2gs/': 'Apple IIGS',
    '/arcadia/': 'Arcadia 2001',
    '/archimedes/': 'Acorn Archimedes',
    '/arduboy/': 'Arduboy',
    '/astrocde/': 'Bally Astrocade',
    '/atari2600/': 'Atari 2600',
    '/atari5200/': 'Atari 5200',
    '/atari7800/': 'Atari 7800',
    '/atari800/': 'Atari 800', # No IGDB* see above


}

def convert_date(date):
    return datetime.strptime(date, '%Y%m%dT%H%M%S')

def import_all_xmls(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('gamelist.xml'):
                file_path = os.path.join(root, file)
                process_xml(file_path)

def get_platform(file_path):
    platform_dict = {platform.name: platform for platform in Platform.objects.all()}

    for scraped_name, igdb_name in SCRAPED_PLATFORM_DICT.items():
        if scraped_name in file_path:
            return platform_dict[igdb_name]

def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for element in root.findall('game'):
        import_game_name = element.find('name').text
        import_file_name = element.find('path').text
        import_release_date = element.find('releasedate').text

        # Grab version number from filename (if version number exists)
        version_match = re.search(r'\(v\d+\.\d+\)', import_file_name)
        import_version = version_match.group(0) if version_match else None 

        if import_version:
            # Remove parentheses for a clean version string
            import_version = import_version.strip("()v")

        # Simple implementation of fuzzy querying to cut down dataset size.
        # If performance becomes an issue, move to a framework like ElasticSearch.
        potential_games = Game.objects.filter(name__icontains=import_game_name[:4])
        best_match = None
        highest_match_score = 0

        for game in potential_games:
            match_score = fuzz.ratio(import_game_name, game.name)
            if match_score > highest_match_score:
                best_match = game
                highest_match_score = match_score

        if highest_match_score >= 95:
            new_game_version = {
                "game": best_match,
                "file_name": import_file_name,
                "release_date": convert_date(import_release_date),
                "version": import_version
            }
        else:
            print(f"No match found for {import_game_name}.")

        filtered_game_version = {key: value for key, value in new_game_version.items() if value is not None}

        GameVersion.objects.get_or_create(**filtered_game_version, is_archived=True)