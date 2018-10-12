# TV Show Indexer

from bs4 import BeautifulSoup
import requests
import json
import sys
import re
import os

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0"}

root_directory = ""
metadata_directory = ""

# IMDB
def imdb_idsearch(showname, imdb_type):
	os.chdir(root_directory)

	if imdb_type.lower() not in ["movie", "tv"]:
		return "Incorrect TYPE"

	types = {"movie": "", "tv": "TV Series"}

	search_link = "https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all"
	search = BeautifulSoup(requests.get(search_link.format(showname.lower().replace(" ", "+")), headers=headers).text, "html.parser")

	t = search.find("table", "findList")
	for y in t.find_all("tr"):
		if types[imdb_type.lower()] in y.text.strip():
			return re.search(r"tt\d\d\d\d\d\d\d", y.a["href"].strip()).group()
		else:
			continue

	return "Unable to locate show"

def imdb_metadata(imdb_id, json_output="n", print_output="y"):
	os.chdir(root_directory)

	if print_output == "y":
		print_output = True
	else:
		print_output = False

	base_url = "https://www.imdb.com/title/{}/episodes?season={}"

	quick = BeautifulSoup(requests.get(base_url.format(imdb_id, "1"), headers=headers).text, "html.parser")
	show_name = quick.find_all("h3", attrs={"itemprop":"name"})[0].a.text.strip()

	tvshow_data = {"show":show_name, "seasons_count":len(quick.select("select#bySeason")[0].find_all("option"))}

	seasons = {}
	for r in range(1, tvshow_data["seasons_count"]+1):
		if print_output:
			print("[\033[94m*\x1B[0m] Fetching season {} of {}".format(r, tvshow_data["seasons_count"]))

		episodes = {}

		show = BeautifulSoup(requests.get(base_url.format(imdb_id, str(r)), headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0"}).text, "html.parser")
		for li in show.find("div", "list detail eplist").find_all("div", "list_item"):
			if "#" not in li.find("div", "info").strong.a.text.strip():
				episodes[str(li.find("div", "info").meta["content"])] = [li.find("div", "info").strong.a.text.strip(), li.find("div", "item_description").text.strip()]

		seasons[r] = episodes

		if print_output:
			print("[\033[92m*\x1B[0m] Downloaded season {} of {}".format(r, tvshow_data["seasons_count"]))

	tvshow_data["seasons"] = seasons

	if json_output == "y":
		with open(metadata_directory + show_name.title().replace(" ", "") + ".json", "w") as j:
			j.write(json.dumps(tvshow_data))

# Media Lookup
def by_senumber(showname, season, episode):
	os.chdir(root_directory)

	showname = showname.lower().title().replace(" ", "")
	season = str(int(season))
	episode = str(int(episode))

	if os.path.exists(metadata_directory + showname + ".json") == False:
		s = imdb_idsearch(showname, "tv")
		m = imdb_metadata(s, json_output="y")

	f = json.loads(open(metadata_directory + showname + ".json").read())

	return f["seasons"][season][episode]

def by_episode(showname):
	os.chdir(root_directory)

	showname = showname.lower().title().replace(" ", "")
	if os.path.exists(metadata_directory + showname + ".json") == False:
		s = imdb_idsearch(showname, "tv")
		m = imdb_metadata(s, json_output="y")

	f = json.loads(open(os.getcwd() + "/tvmetadata/" + showname + ".json").read())

	episodes = {}
	for s in f["seasons"]:
		for e in f["seasons"][s]:
			episodes[f["seasons"][s][e][0]] = [s, e, f["seasons"][s][e][1]]

	return episodes
