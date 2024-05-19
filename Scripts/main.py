from lyricsgenius import Genius

import re
import os

import tkinter as tk
from tkinter import filedialog as fd

from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3

window = tk.Tk()
window.title("LyricsFinder")
window.geometry("700x250")

artist = tk.StringVar()
album = tk.StringVar()
genre = tk.StringVar()
year = tk.StringVar()

directory = ""
songs = []
names = []


class Song:

    filename = ""
    name = ""
    tags = {}

    def __init__(self, file, name):
        self.filename = name
        self.name = namefication(name)

        if '.mp3' in name:
            self.data = EasyMP3(file)
        elif '.flac' in file:
            self.data = FLAC(file)

        self.tags = {
            'album': self.data.tags['album'][0],
            'title': self.data.tags['title'][0],
            'artist': self.data.tags['artist'][0],
            'albumartist': self.data.tags['albumartist'][0],
            'tracknumber': self.data.tags['tracknumber'][0],
            'genre': self.data.tags['genre'][0],
            'date': self.data.tags['date'][0]
        }




def namefication(name):
    newName = deNumber(name)
    newName = re.sub('.flac', '', newName)
    newName = re.sub('.mp3', '', newName)
    return newName


def deNumber(file):
    song = re.sub(r'^\d+.\s*','', file)
    song = re.sub(r'\d*[.]\d* ', "", song)
    return song


def totxt(file):
    txt_name = re.sub('.flac', '.txt', file)
    txt_name = re.sub('.mp3', '.txt', txt_name)
    return txt_name



def chooseAlbum():
    global directory, songs, names
    path = fd.askdirectory()
    if albumPathEntry.get() != "":
       albumPathEntry.delete(0, len(albumPathEntry.get()))
    albumPathEntry.insert(0, path)
    print(path)
    directory = path+"/"
    files = os.listdir(directory)
    songs = []
    names = []
    songList.delete(0, songList.size())
    for file in files:
       if file.endswith(".mp3") or file.endswith(".flac"):
          newSong = Song(directory+file, file)
          songs.append(newSong)

    for i in range(len(songs)):
       songList.insert(i, f"{i+1}. "+songs[i].name)

    artistEntry.delete(0, 100)
    artistEntry.insert(0, songs[0].tags['artist'])

    albumEntry.delete(0, 100)
    albumEntry.insert(0, songs[0].tags['album'])

    genreEntry.delete(0, 100)
    genreEntry.insert(0, songs[0].tags['genre'])

    dateEntry.delete(0, 100)
    dateEntry.insert(0, songs[0].tags['date'])
    print(songs[0].tags)



def findLrcs():
    genius = Genius("You dont really need token for this")
    if artistEntry.get() != "":
        noArtist.config(text="")
        for i in range(len(songs)):
            progressText = f"In Progress... {i+1}/{len(songs)}"
            progress.place(x=126.5, y=230)
            progress.config(text=progressText)
            progress.update()
            try:
                track = genius.search_song(songs[i].tags['title'], songs[i].tags['artist'])

                lrc = track.lyrics
                lrc = re.sub(r'^\d+\s.*?Contributor.*?Lyrics', '', lrc)
                lrc = re.sub(r'See [\w, \s]*? LiveGet tickets as low as \$\d+', '', lrc)
                lrc = re.sub(r'You might also like\w*?\[', '[', lrc)
                lrc = re.sub(r'You might also like\w*?$', "", lrc)
                lrc = re.sub(r'You might also like\n', '', lrc)
                lrc = re.sub(r'\nYou might also like', "\n", lrc)
                lrc = re.sub(r'\[.*?\]\n', '', lrc)
                lrc = re.sub(r'\n\n\n', '\n\n', lrc)
                lrc = re.sub(r'\d*Embed', '', lrc)
                filename = directory + totxt(songs[i].filename)
                print(filename)
                with open(filename, 'w', encoding="utf-8") as file:
                    file.write(lrc)
            except Exception as e:
                print(e)

        progress.config(text="Done!")
        progress.place(x=156.5, y=230)
        progress.update()

    else:
        noArtist.config(text="Specify the artist", foreground="#FF0000")


def setMetaData():
    files = os.listdir(directory)
    i = 1
    for file in files:
       if file.endswith(".flac") or file.endswith(".mp3"):
          tags = ["TITLE", "ARTIST", "ALBUM", "ALBUMARTIST", "GENRE", "DATE", "TRACKNUMBER"]
          values = [deNumber(namefication(file)), artist.get(), album.get(), artist.get(), genre.get(), year.get(), i]
          print(values)
          if ".flac" in file:
             audio = FLAC(directory+file)
          if ".mp3" in file:
             audio = EasyMP3(directory+file)
          for j in range(len(tags)):
             if values[j] != "":
                audio[tags[j]] = f"{values[j]}"

          audio.save()
          i += 1



# ENTRIES
artistEntry = tk.Entry(window, text="", textvariable=artist)
artistEntry.place(x=500, y=31)

albumPathEntry = tk.Entry()
albumPathEntry.place(x=20, y=31)

albumEntry = tk.Entry(window, text = "", textvariable=album)
albumEntry.place(x=500, y=76)

genreEntry = tk.Entry(window, text="", textvariable=genre)
genreEntry.place(x=500, y=121)

dateEntry = tk.Entry(window, text="", textvariable=year)
dateEntry.place(x=500, y=166)


# LABELS
trackList = tk.Label(text="Track List")
trackList.place(x=230, y=10)

artistName = tk.Label(text="Artist")
artistName.place(x=500, y=10)

albumName = tk.Label(text="Album")
albumName.place(x=500, y=55)

genreName = tk.Label(text="Genre")
genreName.place(x=500, y=100)

date = tk.Label(text="Year")
date.place(x=500, y=145)

albumPath = tk.Label(text="Album Path")
albumPath.place(x=20, y=10)

progress = tk.Label()
progress.place(x=131.5, y=230)

noArtist = tk.Label()
noArtist.place(x=20, y=50)


# BUTTONS
chooseAlbumBtn = tk.Button(text="Choose", command=chooseAlbum)
chooseAlbumBtn.place(x=150, y=28)

find = tk.Button(text="Find Lyrics", command=findLrcs)
find.place(x=141.5, y=200)

setMetaDataBtn = tk.Button(text="Set MetaData", command=setMetaData)
setMetaDataBtn.place(x=520, y=200)

#LISTBOXS
songList = tk.Listbox(width=40)
songList.place(x=230, y=30)

window.mainloop()
