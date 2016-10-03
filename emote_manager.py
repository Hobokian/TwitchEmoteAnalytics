# emote_manager.py parses twitch chat and stores emote count in dynamic dictionaries

import json
import urllib.request

dy_lists = []


# Function creates dynamic dictionaries for each channel joined
def create_list_for_each(channel_list):
    global dy_lists
    channel_count = len(channel_list)
    dy_lists = [{} for _ in range(channel_count)]
    for channel in channel_list:
        dy_lists[channel[0]]['channel'] = channel[1]
        get_global_emotes(dy_lists[channel[0]])
        get_sub_emotes((channel[1])[1:], dy_lists[channel[0]])


# Function gets global twitch emotes using available API
def get_global_emotes(channel_obj):
    response = urllib.request.urlopen("https://twitchemotes.com/api_cache/v2/global.json")
    html = response.read()
    parsed = json.loads(str(html, 'utf-8'))
    for x in parsed:
        for y in parsed[x]:
            channel_obj[y] = 0


# Function gets channel specific emotes using available API
def get_sub_emotes(channel_name, channel_obj):
    response = urllib.request.urlopen("https://twitchemotes.com/api_cache/v2/subscriber.json")
    html = response.read()
    parsed = json.loads(str(html, 'utf-8'))
    for x in parsed:
        for y in parsed[x]:
            if y == channel_name:
                chan_emotes = parsed[x].get(y).get("emotes")
                for emote in chan_emotes:
                    emote_name = emote.get('code')
                    channel_obj[emote_name] = 0


# Function counts emotes used for each channel joined
def emote_counter(chan_and_msg):
    channel = chan_and_msg[0]
    msg = chan_and_msg[1]
    for chan_in_list in dy_lists:
        if channel == chan_in_list['channel']: # Check channel name
            index = dy_lists.index(chan_in_list)
            for i, emote in enumerate(dy_lists[index]):
                if emote in msg and emote not in channel:
                    try:
                        dy_lists[index][emote] += msg.count(emote)
                    except TypeError:
                        continue

