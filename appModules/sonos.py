# -*- coding: UTF-8 -*-
# Sonos: a NVDA appModule for Sonos Desktop, Version 1.5
#Copyright (C) 2019/2020 Ralf Kefferpuetz, other contributors
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
from NVDAObjects.UIA import ListItem, UIA
import time

"""
NVDA appModule for Sonos Desktop
Adds several hotkeys:
- control-1 - speaks current roomname, stationname and title of song
- double press alt-1 - copies song title to the clipboard
- control-2 - opens the song title in a virtual invisible window to read it back
- control-3 - opens Youtube in your default browser with the results for currently playing song (opens in a new tab)
- alt-shift-v  - reports current volume
- alt-shift-m  - reports mute status
- control-m - toggles mute
- alt-shift-r  - reports repeat status
- control-r - toggles repeat
- alt-shift-e  - reports shuffle status
- control-e - toggles shuffle
- alt-shift-t  - reports crossfade status
- control-t - toggles crossfade
- alt-shift-u  - reports time playing
- alt-shift-i  - reports scrub
- alt-shift-o  - reports play time left
- makes the Sonos shortCuts window accessible (control-k)
"""

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_DATAITEM:
			clsList.insert(0, TBGrid)

	def script_speakInfo(self, gesture):
		try:
			fg = api.getForegroundObject()
			s2 = fg.firstChild.next.next.next.next.next.firstChild.next.name
			s3 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.name
			s4 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.name
			s7 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.name
			s8 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.name
			if not s8: s7 = ""
			s5 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			s6 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			infoString = (" %s %s %s %s %s %s %s" % (s2, s3, s4, s7, s8, s5, s6))
			infoString2 = (" %s %s %s %s %s %s %s" % (s2, s3, s4, s7, s8, s5, s6))
			#infoString2 = s2+" - "+s4+" - "+s6
			infoString3 = ("%s %s %s %s %s %s" % (s3, s4, s7, s8, s5, s6))
			#infoString3 = s4+" - "+s6
			if scriptHandler.getLastScriptRepeatCount() == 1:
				#double press
				api.copyToClip(infoString3)
				tones.beep(1500, 120)
			else:
				num=int(gesture.mainKeyName[-1])
				if num == 2:
					if not s6: s6 = "no song information found!"
					if not s4: s4 = "no station information found!"
					ui.browseableMessage(infoString2, title="Now playing on " + s4, isHtml=False)
				else:
					ui.message(infoString)
		except AttributeError:
			pass
	# Translators: Documentation for speakInfo script.
	script_speakInfo.__doc__=_("speaks Sonos roomname, artist and songtitle, double press copies it to the clipboard. alt-2 shows the title in a hidded browseable message.")

	def script_openInYoutube(self, gesture):
		try:
			fg = api.getForegroundObject()
			s2 = fg.firstChild.next.next.next.next.next.firstChild.next.name
			s3 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.name
			s4 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.name
			s7 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.name
			s8 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.name
			if not s8: s7 = ""
			s5 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			s6 = fg.firstChild.next.next.next.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			infoString3 = ("%s %s %s %s %s %s" % (s3, s4, s7, s8, s5, s6))
			if infoString3: #do nothing if no song is playing or if song title is not available
				# following replacement is necessary because youtube search does not accept the & sign
				infoString3 = infoString3.replace("&", " ")
				url = "https://www.youtube.com/results?search_query="+infoString3
				webbrowser.open_new_tab(url) # opens in default browser
		except:
			pass
	# Translators: Documentation for openInYoutube script.
	script_openInYoutube.__doc__=_("opens Youtube in your default browser with the search results of the currently playing song.")

	def script_reportVolume(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.name
			s2 = fg.firstChild.next.next.firstChild.next.next.value
			s1 = s1+": "+s2+"%"
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportVolume script.
	script_reportVolume.__doc__=_("reports the volume of the active room.")

	def script_reportMute(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.description
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportMute script.
	script_reportMute.__doc__=_("reports the mute status of the active room.")

	def script_toggleMute(self, gesture):
		try:
			gesture.send()
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next
			if controlTypes.STATE_PRESSED not in s1.states:
				ui.message("on")
			if controlTypes.STATE_PRESSED  in s1.states:
				ui.message("off")
		except:
			pass
	# Translators: Documentation for toggleMute script.
	script_toggleMute.__doc__=_("toggles mute for  the active room.")


	def script_reportRepeat(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.description
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportRepeat script.
	script_reportRepeat.__doc__=_("reports the mute status of the active room.")

	def script_toggleRepeat(self, gesture):
		try:
			gesture.send()
			time.sleep(1)   # Delays for 5 seconds. 
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next
			if controlTypes.STATE_PRESSED not in s1.states:
				ui.message("off")
			if controlTypes.STATE_PRESSED  in s1.states:
				ui.message("on")
		except:
			pass
	# Translators: Documentation for toggleRepeat script.
	script_toggleRepeat.__doc__=_("toggles repeat  of the active room.")


	def script_reportShuffle(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.description
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportShuffle script.
	script_reportShuffle.__doc__=_("reports the shuffle status of the active room.")

	def script_toggleShuffle(self, gesture):
		try:
			gesture.send()
			time.sleep(1)   # Delays for 5 seconds. 
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next
			if controlTypes.STATE_PRESSED not in s1.states:
				ui.message("off")
			if controlTypes.STATE_PRESSED  in s1.states:
				ui.message("on")
		except:
			pass
	# Translators: Documentation for toggleShuffle script.
	script_toggleShuffle.__doc__=_("toggles shuffle  of the active room.")


	def script_reportCrossfade(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.description
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportCrossfade script.
	script_reportCrossfade.__doc__=_("reports the crossfade status of the active room.")

	def script_toggleCrossfade(self, gesture):
		try:
			gesture.send()
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next
			if controlTypes.STATE_PRESSED not in s1.states:
				ui.message("off")
			if controlTypes.STATE_PRESSED  in s1.states:
				ui.message("on")
		except:
			pass
	# Translators: Documentation for toggleCrossfade script.
	script_toggleCrossfade.__doc__=_("toggles crossfade  of the active room.")


	def script_reportCurrent(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportCurrent script.
	script_reportCurrent.__doc__=_("reports the current track time of the active room.")

	def script_reportScrub(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			s2 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.value
			s1 = s1+": "+s2+"%"
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportScrub script.
	script_reportScrub.__doc__=_("reports the current scrubbing index of the played song.")

	def script_reportRemaining(self, gesture):
		try:
			fg = api.getForegroundObject()
			s1 = fg.firstChild.next.next.firstChild.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.name
			ui.message(s1)
		except:
			pass
	# Translators: Documentation for reportRemaining script.
	script_reportRemaining.__doc__=_("reports the current scrubbing index of the played song.")


	__gestures = {
		"kb:control+1": "speakInfo",
		"kb:control+2": "speakInfo",
		"kb:control+3": "openInYoutube",
		"kb:alt+shift+v": "reportVolume",
		"kb:alt+shift+m": "reportMute",
		"kb:control+m": "toggleMute",
		"kb:alt+shift+r": "reportRepeat",
		"kb:control+r": "toggleRepeat",
		"kb:alt+shift+e": "reportShuffle",
		"kb:control+e": "toggleShuffle",
		"kb:alt+shift+t": "reportCrossfade",
		"kb:control+t": "toggleCrossfade",
		"kb:alt+shift+u": "reportCurrent",
		"kb:alt+shift+i": "reportScrub",
		"kb:alt+shift+o": "reportRemaining"
	}

class TBGrid(ListItem):
# tis to make the Sonos shortCuts window accessible. Makes the listview readable as a normal listview (control-k)

	def event_gainFocus(self):
		fg = api.getFocusObject()
		if fg.name.startswith('Sonos.Controller.Desktop.Main.KeyboardShortcut'):
			shortkeys = (" %s %s" % (fg.firstChild.name, fg.firstChild.next.name))
			fg.name = shortkeys
			ui.message(shortkeys)
			return
		super(TBGrid,self).event_gainFocus()

