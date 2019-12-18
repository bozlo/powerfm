#!/usr/local/bin/python
# coding=utf-8
#
# Add ID3Tag
# bozloo@hotmail.com 12/17/2019
#
import eyed3
import sys

reload(sys)  
sys.setdefaultencoding('utf8')


def Add_id3tag(filename, title, album, artist, album_artist, genre):
	try:
		f = eyed3.load(filename)
		f.initTag()
		
		if title:
			f.tag.title = title

		if album:
			f.tag.album = album
	
		if artist:
			f.tag.artist = artist

		if album_artist:
			f.tag.album_artist = album_artist

		if genre:
			f.tag.genre = genre

		# Store
		f.tag.save()
	except IOError as error:
		print error
		return False

	return True

