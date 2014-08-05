#!/usr/bin/env python

import feedparser
import re
import os, subprocess
import sys
from termcolor import cprint

query = input("Which Anime are you looking for?\n")

search = feedparser.parse('http://www.nyaa.se/?page=search&cats=1_37&filter=0&term=' + query + '&page=rss&sort=2')

# Group #0 - Number of Seeders | Group #1 - Number of Leechers | Group #2 - Number of Downloads | Group #3 - Size in KiB|MiB|GiB
regex = re.compile("(\d*) seeder\(s\), (\d*) leecher\(s\), (\d*) download\(s\) - (\d*(?:\.\d*)? (?:KiB|MiB|GiB))(.*)")

print(len(search.entries))

for i in range(0, len(search.entries)):
	file = search.entries[i]
	elems = regex.match(file.summary)
	print(	"[" + str(i) + "]\t" + file.title, end="\n\t")
	cprint(	"SE " + elems.group(1), 'green', attrs=['bold'], end="\t"),
	cprint(	"LE " + elems.group(2), 'red', attrs=['bold'], end="\t")
	print(	"Size " + elems.group(4))

digits = input("select files:\n").split()

NULLF = open(os.devnull, 'w')
def download(n):
	print("Adding torrent...", subprocess.call(["transmission-remote-cli", search.entries[n].link], stdout=NULLF))

running = subprocess.call(["pidof", "transmission-daemon"])
print("'transmission-daemon' is running?...", running)
if running != 0:
	print("Trying to start 'transmission-daemon'...", subprocess.call("transmission-daemon"))

for number in digits:
	if '-' in number:
		mrange = number.split('-')
		print("adding files ", mrange[0], "to", mrange[1])
		for i in range(int(mrange[0]), int(mrange[1]) + 1):
			download(i)
	else:
		download(int(number))
