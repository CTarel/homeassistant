#!/usr/bin/python
import sys
import http.cookiejar, urllib.request, urllib.error, urllib.parse
import json
import codecs

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

IP_syno = "IP_OF_YOUR_NAS"
LOGIN = "********"
PASSWORD = "********"
player = sys.argv[1]

opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),
    ]

#URL to send requests to Synology
urlAuth = "http://" + IP_syno + ":5000/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=" + LOGIN + "&passwd=" \
+ PASSWORD + "&session=AudioStation&format=cookie"
urlPlayers = "http://" + IP_syno + ":5000/webapi/AudioStation/remote_player.cgi?api=SYNO.AudioStation.RemotePlayer&version=1&method=list"
opener.open(urlAuth)

#Get Players list as JSON
pagePlayers = opener.open(urlPlayers)
strPlayers = codecs.getreader(pagePlayers.headers.get_content_charset())
jsonPlayers = json.load(strPlayers(pagePlayers))['data']['players']
#print(jsonPlayers)

#Get Player ID required to send http command to play content on the chosen player on Synology
for d in jsonPlayers:
 PlayerName = d['name']
 if PlayerName == player:
  PlayerID = d['id']

urlStop = "http://" + IP_syno + ":5000/webapi/AudioStation/remote_player.cgi?api=SYNO.AudioStation.RemotePlayer&method=control&action=stop&id=" + PlayerID + "&version=$
#print(urlStop)
opener.open(urlStop)
