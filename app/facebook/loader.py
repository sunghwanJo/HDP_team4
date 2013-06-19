# -*- coding: utf-8 -*-

import re
import imp
import os.path
import os
import json
import urllib2
import httplib
import time
page = urllib2.urlopen("http://www.nextstudents.nazuka.net/facebook/load_token.php")
load_page = page.read().decode("utf8")

split_temp = []
split_temp = load_page.split(" <scrip")

ACCESS_TOKEN = split_temp[0]

#ACCESS_TOKEN = 'CAACjeiZB6FgIBAGdZB0vZC3ePZBlMSL722hRtZCZAzHi2FwplZCo9ta7C7IK9NELyJxW4SpaKkUQoZArlclWZBjDS6Wxca0c2foTl55iKMMzp4bV0E4Y5ZATl2yOR3peCjZAj2wr8ddOm6rcJPlunaDTrrPcaKZA2v6OBwMZD'

class facebook_parsing:
	
	def __init__(self):
		self.LOCAL_FILE = 'app.facebook.fb_access_token'
		self.pf_list = ["이익훈", "강성훈","구승모", "김동진", "김종규","박재성","서경진","손영수","오동우","윤지수","이남영","임석현","정호영","조혜연","주형철","함석진","Euntaek Hong","김평철"]
		self.teacher_list = ["소라","안현진","Bongsu Cho","Lena Park","박순영","김현진","Eunhee Seo","이세현"]
		
	def parse_facebook(self):
		
		try:
			self.cafe_data_dict = {}
			debug_url = "a"
			debug_url = 'https://graph.facebook.com/132468483587501?fields=feed.fields(message,created_time,link,from,id)&access_token=' + ACCESS_TOKEN
			debug_url = debug_url.encode('utf8')
			debug_url = debug_url[:-3]
			
			u = urllib2.urlopen(debug_url)

			time.sleep(1)

			self.cafe_data_dict = json.load(u)
			u.close()
		except:
			pass

	def fout_posts(self):		
		data_list = []
		cafe_data_dict ={}
		cafe_data_dict = self.cafe_data_dict
		for data in cafe_data_dict["feed"]["data"]:
			try:
				category = u""
				if( data["from"]["name"].encode('utf8') in self.pf_list )	:
					category = u"교수님글"
				elif( data["from"]["name"].encode('utf8') in self.teacher_list ) 	:
					category = u"선생님글"
				else:
					category = u"기타"

				#print data["message"].encode('utf8')
				data_list.append(["http://www.facebook.com/"+data["id"].encode('utf8'),"facebook","na우리next",data["message"].encode('utf8').split("\n")[0][0:128],data["created_time"].encode('utf8'),data["from"]["name"].encode('utf8'),category])
			except:
				pass
		return data_list


#fb = facebook_parsing()
#fb.parse_facebook()
#fb.fout_posts()



