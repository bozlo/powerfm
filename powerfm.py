#!/usr/local/bin/python
# coding=utf-8
#
# PowerFM Radio download program
# bozloo@hotmail.com 12/17/2019
#
import re
import os
import sys
import requests
from requests.exceptions import HTTPError
import json
import id3tag

#handle unicode
reload(sys)
sys.setdefaultencoding('utf8')

# constant
vod_id = ''
startPage = 1					# 1 means the latest page

DL_ALL = ' '				 	# download All
DL_YEAR = '365'					# almost a year
DL_MONTH = '31'					# a month 
DL_CUSTOM = '10'
itemPerPage = DL_CUSTOM

# Radio Station
youngcheol_station = {u'무식탈출영철쇼': 'V2000009986', u'진짜 미국식 영어': 'V2000010062', u'다시 듣기': 'V2000009984'}
cultwoshow_station = {u'컬튜쇼':'V0000328482', u'레전드 사연':'V0000364436'}
cinetown_station = {u'씨네타운':'V2000008804'}
morningchang_station = {u'아름다운 이 아침':'V0000010355'}

all_stations = {u'영철쇼': youngcheol_station, u'컬튜쇼':cultwoshow_station, u'박선영':cinetown_station, u'김창완':morningchang_station}


# select station and section to download
selected_sections = [{u'station':u'영철쇼', u'section':u'무식탈출영철쇼'}, {u'station':u'박선영', u'section':u'씨네타운'}]

# create folder
def create_folder(name):
	try: 
		if not os.path.exists(name):
			os.mkdir(name) 
	except OSError as error: 
		print('%s\n[folder] Error in creating folder : %s' % (error, name))
		return False

# main loop
for content in selected_sections:
	station = ''
	section = ''

	try:
		station = content[u'station']
		section = content[u'section']

		vod_id = all_stations[station][section]
		print('Select %s of %s ...' % (section, station))
	except KeyError:
		print('Cant find \"%s\" section in the \"%s\" station' % (section, station))
		continue

	# Core download module
	listUrl = "https://apis.sbs.co.kr/radio-api/podcast/podcast_list_json"
	headers = {'content-type': 'application/json; charset=utf-8'}
	params = {'vod_id':vod_id, 'page':startPage, 'item_per_page':itemPerPage}

	create_folder(station)
	create_folder(station+'/'+section)

	try:
		r = requests.get(listUrl, params=params, headers=headers);

		# If the response was successful, no Exception will be raised
		r.raise_for_status()
	except HTTPError as http_err:
		print('[list] HTTP error occurred: %s' % http_err)
	except Exception as err:
		print('[list] Other error occurred: %s' % err)
	else:
		r.close()

		itr = 0
		for x in r.json()['data']:
			itr += 1
			try:
				url = x['UPLOAD_URL']
				fn = x['CON_TITLE'].strip()
				dn = x['BROAD_DATE']
				fn = re.sub(r'- \d+\.\d+\.\d+', '', fn)
				fn = fn + ' - ' + dn
				filename = station + '/' + section + '/' + fn + '.mp3'
			except:
				print('Parse error')
				print(json.dumps(x, ensure_ascii=False))
				print
				continue

#   for debug ----------------------------------------------
#			if itr == 309:
#				print(json.dumps(x, ensure_ascii=False))

#			print('[%s] %s' % (itr,filename))
#			continue
# ----------------------------------------------------------

			if os.path.exists(filename):
				print('[download] file exists. Skip %s' % filename)
				continue

			try:
				r = requests.get(url)
				with open(filename, 'wb') as f:
					f.write(r.content);		
				r.raise_for_status()
			except HTTPError as http_err:
			  print('[download] HTTP error occurred: %s' % http_err)
			except Exception as err:
			  print('[download] Other error occurred: %s' % err)
			else:
				print('[download] Download %s and store to %s' % (url, filename))
				r.close()
				
				# Change ID3Tag
				title = filename[:-4]
				album = section
				artist = station
				album_artist = station + '-' + section
				genre = u'Vocal'
				id3tag.Add_id3tag(filename, title, album, artist, album_artist, genre)

		print('\nDone')


