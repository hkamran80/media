# Metadata+ Functions

import mediaindex
import re

# Edit this variable to match your image directory
artwork_directory = ""
artwork = {}

def prep_file(ep_file):
	if ".mp4" in ep_file:
		ep = ep_file.replace(".mp4", "")
	else:
		ep = ep_file

	return ep

# Actual MP+ Functions
def marvelhq(ep, show):
	ep = prep_file(ep)

	if show == "Guardians of the Galaxy":
		se = re.search(r"S\d Ep\d", ep).group()

		s = se.split(" ")[0].strip("S")
		e = se.split(" ")[1].strip("Ep")

		synopsis = mediaindex.by_senumber(show, s, e)[1]

		return [season, episode_num, synopsis, show]

def flash(ep):
	ep = prep_file(ep)
	show = "The Flash"

	show_episodes = mediaindex.lookup(show)
	episode_data = show_episodes[ep]

	season = episode_data[0]
	episode_num = episode_data[1]
	synopsis = episode_data[2]

	return [season, episode_num, synopsis, show]
