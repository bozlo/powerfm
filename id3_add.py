#!/usr/local/bin/python
# coding=utf-8
#
# Add ID3Tag
# bozloo@hotmail.com 12/17/2019
#
import eyed3
import sys
import os

reload(sys)  
sys.setdefaultencoding('utf8')

title = u''
album = u''
artist = u''
album_artist = u''
genre = u''

try:
	album = '무식탈출영철쇼'
	artist = '김영철'
	album_artist = '김영철-무식탈출영철쇼'
	genre = 'Vocal'
except IndexError:
	pass

lists = filter(lambda x: x.endswith('.mp3'), os.listdir('.'))

for x in lists:
	try:
		print('load %s' % x)
		f = eyed3.load(x)
		f.initTag()
		
		title = x[:-4]
		if title:
			f.tag.title= unicode(title, 'utf-8')

		if album:
			f.tag.album = unicode(album, 'utf-8')
	
		if artist:
			f.tag.artist= unicode(artist, 'utf-8')

		if album_artist:
			f.tag.album_artist = unicode(album_artist, 'utf-8')

		if genre:
			f.tag.genre = unicode(genre, 'utf-8')

		# Store
		f.tag.save()
	except IOError as error:
		print('error here')
		print error
		continue

exit(0)
