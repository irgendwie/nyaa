#!/usr/bin/env python
import feedparser
import re
from termcolor import cprint
import signal
from subprocess import call
from sys import exit,argv
from os import devnull
import constants

def signal_handler(signal, frame):
	exit(1)
signal.signal(signal.SIGINT, signal_handler)

# 1. #Seeders - 2. #Leechers - 3. #Downloads - 4. Size - 5. Additional
rss_regex = re.compile("(\d+) seeder\(s\), (\d+) leecher\(s\), (\d+) download\(s\) - (\d+(?:\.\d+)? (?:KiB|MiB|GiB))(.*)")

if len(argv) > 1:
    search_query = ' '.join(argv[1:])
else:
    search_query = input("Which Anime are you looking for?\n>> ")
search_url = constants.URL + "&cats=" + constants.CATS_ANIME_ENGLISH_TRANSLATED + "&filter=" + constants.FILTER_NONE + "&order=" + constants.ORDER_DESCENDING + "&sort=" + constants.SORT_SEEDERS + "&term=" + search_query
search_result = feedparser.parse(search_url)

# Printing search results
for i in range(0, len(search_result.entries)):
	regex_match = rss_regex.match(search_result.entries[i].summary)
	cprint("[" + str(i) + "]", end='\t')
	if "Trusted" in regex_match.group(5):
		if "A+" in regex_match.group(5):
			cprint(search_result.entries[i].title, 'blue')
		else:
			cprint(search_result.entries[i].title, 'green')
	else:
		if "Remake" in regex_match.group(5):
			cprint(search_result.entries[i].title, 'yellow')
		else:
			print(search_result.entries[i].title)
	cprint("\tSize " + regex_match.group(4), end='\t')
	cprint("SE " + regex_match.group(1), 'green', end='\t')
	cprint("LE " + regex_match.group(2), 'red', end='\t')
	cprint("DLs " + regex_match.group(3))

numbers = input("Choose files to download\n>> ").split()

if not numbers:
	exit(0)
else:
	NULLF = open(devnull, 'w')
	# Starting 'transmission-daemon', if not already running!
	if call(["pidof", "transmission-daemon"], stdout=NULLF) == 1:
		cprint("Starting 'transmission-daemon'... ", end='')
		td_running = call("transmission-daemon", stdout=NULLF)
		while(td_running == 1):
			cprint("failed\nRetrying... ", end='')
			td_running = call("transmission-daemon", stdout=NULLF)
		cprint("done")
	# Download
	for digit in numbers:
		s_digit = digit.split('-')
		if len(s_digit) == 2:
			for n in range(int(s_digit[0]), int(s_digit[1]) + 1):
				cprint("Adding file " + str(n) + "...", end='')
				call(["transmission-remote-cli", search_result.entries[int(n)].link], stdout=NULLF)
				cprint("done")
		else:
			cprint("Adding file " + str(digit) + "...", end='')
			call(["transmission-remote-cli", search_result.entries[int(digit)].link], stdout=NULLF)
			cprint("done")
