# twitch_chatbot.py joins channels, reads twitch chat, and calls a chat parser

import re
import socket
import sys
import getopt
import emote_manager
import json


# Function get_args takes in channel names [-c channel1 channel2]
def get_args(argv):
    try:
        opts, args = getopt.getopt(argv, "c", ["channels="])
        if args == []:
            print('bot.py -c <channel name>')
            sys.exit(2)
    except getopt.GetoptError:
        print('bot.py -c <channel name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-c":
            print(arg)
            global CHAN
            CHAN = args
            print("Attempting to connect to:" + str(CHAN))
            return CHAN

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.chat.twitch.tv"                     # Hostname of the IRC-Server in this case twitch's
PORT = 80                                       # Default IRC-Port
CHAN = ""                                       # List of channel names = {Nickname, Nickname, etc.}
NICK = ""                                       # Nickname = Twitch username
PASS = "oauth:"                                 # www.twitchapps.com/tmi/ will help to retrieve the required authkey
CONNECTED_CHANNELS = []
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channels(chans):
    for channel in chans:
        con.send(bytes('JOIN %s\r\n' % channel[1], 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    if len(msg) >= 1:
        result = ""
        i = 3
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        temp_tuple = [msg[2], result]
        return temp_tuple


def parse_message(chan_and_msg):
    if len(chan_and_msg) >= 1:
        emote_manager.emote_counter(chan_and_msg)


def create_channels(channels):
    for i,channel in enumerate(channels):
        channel = "#" + channel
        temp_tuple = [i, channel]
        CONNECTED_CHANNELS.append(temp_tuple)
        print("Connected to " + str(channel))

# --------------------------------------------- End Helper Functions -----------------------------------------------
con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
CHAN = get_args(sys.argv[1:])
create_channels(CHAN)
emote_manager.create_list_for_each(CONNECTED_CHANNELS)
join_channels(CONNECTED_CHANNELS)


data = ""

while True:
    try:
        data = data+con.recv(2048).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
            try:
                if len(line) >= 1:
                    if line[0] == 'PING':
                        send_pong(line[1])

                    if line[1] == 'PRIVMSG':
                        sender = get_sender(line[0])
                        message = get_message(line)
                        parse_message(message)
                        with open('F:/Website/Projects/WebServer/Version1/data.json', 'w') as outfile:
                            json.dump(emote_manager.dy_lists, outfile)
            except IndexError:
                continue

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")