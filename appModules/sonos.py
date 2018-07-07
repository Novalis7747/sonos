# -*- coding: UTF-8 -*-
# Sonos: a NVDA appModule for Sonos Desktop, Version 1.00
#Copyright (C) 2018 Ralf Kefferpuetz, other contributors
# Released under GPL 2

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import speech
import controlTypes
import ui
import api
import webbrowser
import tones
import scriptHandler

"""
NVDA appModule for Sonos Desktop
Adds 3 hotkeys:
- control-1 - speaks current roomname, stationname and title of song
- double press alt-1 - copies song title to the clipboard
- control-2 - opens the song title in a virtual invisible window to read it back
- control-3 - opens Youtube in your default browser with the results for currently playing song (opens in a new tab)
"""

class AppModule(appModuleHandler.AppModule):

	def script_speakInfo(self, gesture):
		try:
			fg = api.getForegroundObject()
			# this is the room name
			s2 = fg.firstChild.next.next.next.next.next.next.next.next.firstChild.next.name
			# this is the station playing
			s4 = fg.firstChild.next.next.next.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.name
			# this is the song title currently playing
			s6 = fg.firstChild.next.next.next.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			infoString = (" %s - %s: %s" % (s2, s4, s6))
			infoString2 = s2+"\n"+s4+"\n"+s6
			if scriptHandler.getLastScriptRepeatCount() == 1:
				#double press
				api.copyToClip(s6)
				tones.beep(1500, 120)
			else:
				num=int(gesture.mainKeyName[-1])
				if num == 2:
					if not s6: s6 = "no song information found!"
					ui.browseableMessage(s6, title="Now playing on " + s4, isHtml=False)
				else:
					ui.message(infoString)
		except AttributeError:
			pass
	# Translators: Documentation for speakInfo script.
	script_speakInfo.__doc__=_("speaks Sonos roomname, artist and songtitle, double press copies it to the clipboard. alt-2 shows the title in a hidded browseable message.")

	def script_openInYoutube(self, gesture):
		try:
			fg = api.getForegroundObject()
			s6 = fg.firstChild.next.next.next.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			if s6: #do nothing if no song is playing or if song title is not available
				# following replacement is necessary because youtube search does not accept the & sign
				s6 = s6.replace("&", " ")
				url = "https://www.youtube.com/results?search_query="+s6
				webbrowser.open_new_tab(url) # opens in default browser
		except:
			pass
	# Translators: Documentation for openInYoutube script.
	script_openInYoutube.__doc__=_("opens Youtube in your default browser with the search results of the currently playing song.")

	__gestures = {
		"kb:control+1": "speakInfo",
		"kb:control+2": "speakInfo",
		"kb:control+3": "openInYoutube"
	}

