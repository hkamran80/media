# TV Show Metadata+

import mediaindex
import handycode
import mp_func
import os

cmd = """ AtomicParsley "{}/{}.mp4" --title "{}" --TVShowName "{}" --TVSeason {} --TVEpisodeNum {} --description "{}" --stik "TV Show" --artwork "{}" -o "{}/{}.mp4" """

directory_split = "|"
base_directory = ""

def prep_file(ep_file):
	if ".mp4" in ep_file:
		ep = ep_file.replace(".mp4", "")
	else:
		ep = ep_file

	return ep

if __name__ == "__main__":
	directories = input("Directories (seperated by \"{}\", base directory: \"{}\"): ".format(directory_split, base_directory))
	for directory in directories.split(directory_split):
		directory = base_directory + directory
		print(directory)
		os.chdir(directory)

		for ep in handycode.listdir(os.getcwd()):
			ep = prep_file(ep)

			print("[\033[94m*\x1B[0m] Adding metadata to '{}'".format(ep))

			if os.path.exists(base_directory + "tvshows/{}/S{}/".format(show.replace(" ", ""), s)):
				pass
			else:
				os.makedir(base_directory + "tvshows/{}/S{}/".format(show.replace(" ", ""), s))

			m = os.system(cmd.format(base_directory, "{}/".format(dir_loc) + ep, ep, show, s, e, synopsis, artwork[show.replace(" ", "") + "_S{}".format(s)], base_directory, "tvshows/{}/S{}/S{}E{}".format(show.replace(" ", ""), s, s, e)))
			
			print("[\033[92m*\x1B[0m] Metadata added to '{}'".format(ep))
