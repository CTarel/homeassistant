#!/usr/bin/python
import sys
import http.cookiejar, urllib.request, urllib.error, urllib.parse
import json
import codecs

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
IP_syno = "IP OF YOUR NAS"
LOGIN = "**********"
PASSWORD = "********"

# When calling the script in command line, pass two arguments: playlist and player (ie cmd line must be 'python3 playlist.py
# playlist player')
playlist = sys.argv[1]
player = sys.argv[2]
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),
    ]

#URL to send requests to Synology
urlAuth = "http://" + IP_syno + ":5000/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=" + LOGIN + "&passwd=" \
+ PASSWORD + "&session=AudioStation&format=cookie"
urlPlayers = "http://" + IP_syno + ":5000/webapi/AudioStation/remote_player.cgi?api=SYNO.AudioStation.RemotePlayer&version=1&method=list"
urlPlaylists = "http://" + IP_syno + ":5000/webapi/AudioStation/playlist.cgi?api=SYNO.AudioStation.Playlist&version=2&method=list"
opener.open(urlAuth)

#Get Players list as JSON
pagePlayers = opener.open(urlPlayers)
strPlayers = codecs.getreader(pagePlayers.headers.get_content_charset())
jsonPlayers = json.load(strPlayers(pagePlayers))['data']['players']
#print(jsonPlayers)

#Get Playlists list as JSON
pagePlaylists = opener.open(urlPlaylists)
strPlaylists = codecs.getreader(pagePlaylists.headers.get_content_charset())
jsonPlaylists = json.load(strPlaylists(pagePlaylists))['data']['playlists']
#print(jsonPlaylists)

#Get Player ID required to send http command to play content on the chosen player on Synology
for d in jsonPlayers:
 PlayerName = d['name']
 if PlayerName == player:
  PlayerID = d['id']
  #print(PlayerID)

#Get Playlist ID required to send http command to play the chosen playlist on Synology
for d in jsonPlaylists:
 PlaylistName = d['name']
 if PlaylistName == playlist:
  PlaylistID = d['id']

#Params
jsonStr = '[{"type":"playlist","id":"%s"}]' % PlaylistID
#print(jsonStr)
params = [('api', 'SYNO.AudioStation.RemotePlayer'),
             ('method', 'updateplaylist'),
             ('library', 'shared'),
             ('id', PlayerID),
             ('offset', '0'),
                         ('limit', '0'),
                         ('play', 'true'),
             ('version', '2'),
             ('containers_json', jsonStr),
           ]
#Load
urlLoad = urllib.parse.urlencode(params)
httpLoadReq = "http://" + IP_syno + ":5000/webapi/AudioStation/remote_player.cgi?" + urlLoad
#print(urlLoad)
opener.open(httpLoadReq)
#Play
urlPlay = "http://" + IP_syno + ":5000/webapi/AudioStation/remote_player.cgi?api=SYNO.AudioStation.RemotePlayer&method=control&id=" + PlayerID + \
"&version=2&action=play&value=0"
opener.open(urlPlay)
#Logout
urlLogout = "http://" + IP_syno + ":5000/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=AudioStation"
opener.open(urlLogout)

