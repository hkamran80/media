"""
Spotify Current Track Metadata
Platform: macOS
Contributors:
	:: H. Kamran [@hkamran80] (author)

Last Updated: 2018-11-08, @hkamran80
"""

try:
	from Foundation import *
except ImportError:
	from CoreFoundation import *

getCurrentTrack = """
set currentlyPlayingTrack to getCurrentlyPlayingTrack()
displayTrackData(currentlyPlayingTrack)

on getCurrentlyPlayingTrack()
	tell application "Spotify"
		set currentTrack to name of current track as string
		set currentAlbum to album of current track as string
		set currentArtist to artist of current track as string

		return currentArtist & " - " & currentTrack & " -- " & currentAlbum
	end tell
end getCurrentlyPlayingTrack

on displayTrackData(trackData)
	copy trackData to stdout
end displayTrackData
"""

applescript = str(NSAppleScript.alloc().initWithSource_(getCurrentTrack).executeAndReturnError_(None))

as_utxt = applescript[applescript.find("(\"")+2:applescript.find("\")")]

track = {}

track["track"] =  as_utxt.split(" - ")[1].split(" -- ")[0]
track["artist"] = as_utxt.split(" - ")[0]
track["album"] =  as_utxt.split(" -- ")[1]

print(track)
