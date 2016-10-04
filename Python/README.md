# TwitchEmoteAnalytics Python

Python code includes:
- Chat bot [python_twitch_chatbot.py]
	- Takes a single or multiple argument(s) -c to join channel(s) 
		- [Example: $ python python_twitch_chatbot.py -c summit1g]
	- Joins channel(s) chat and calls chat parser
- Chat parser [emote_manager.py]
	- Gets twitch.tv global emotes
	- Gets twitch.tv channel specific emotes (if any)
	- Parses chat messages for emotes and stores emote count in dynamic dictionaries
- Flask web service [service.py]
	- Reads a json file and creates an API allowing for use on HTML pages
