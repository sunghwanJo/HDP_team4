#-*- coding:utf-8 -*-
from app import db
from app.cafe.cafe_parsing2 import *
from app.facebook.loader import *
"""
class user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	password = db.Column(db.String(30))
	def __init__(self, name, password):
		self.name = name
		self.password = password
"""

class parsing_data(db.Model):
	url = db.Column(db.String(250), primary_key = True)					#게시글의 url address
	site = db.Column(db.String(20))					#Cafe facebook 구분
	location = db.Column(db.String(100))			#까페내 게시판 이름(facebook에서는 "나우리넥스트"
	title = db.Column(db.String(200))				#글 제목(facebook에서는 글의 첫문장)
	datetime = db.Column(db.String(50))				#작성일 작성시간
	username = db.Column(db.String(50))				#작성자
	category = db.Column(db.String(50))		#게시글 분류
	def __init__(self, url,site,location,title,datetime,username,category):
		self.url = url
		self.site = site
		self.location = location
		self.title = title
		self.datetime = datetime
		self.username = username
		self.category = category
	
	"""
	def __repr__(self):
		return '%s' %self.url

	def db_create(self):
		db.create_all()
		return "!!"

	def db_insert(self,url,site,location,title,datetime,username,category):
		data = parsing_data(url,site,location,title,datetime,username,category)
		db.session.add(data)
		db.session.commit()
		return "@@"

	def db_insert_cafe(self):
		cp = cafe_parsing()
		cp.split_data()
		load_list = []
		load_list = cp.fout_post()
		str_return = "cafe_parsing"
		for load in load_list:
			try:
				datas = parsing_data(load[0].decode('utf8'),load[1].decode('utf8'),load[2].decode('utf8'),load[3].decode('utf8'),load[4].decode('utf8'),load[5].decode('utf8'),load[6])
				db.session.add(datas)
				db.session.commit()
			except:
				pass
		return str_return

	def db_insert_facebook(self):
		fp = facebook_parsing()
		fp.parse_facebook()
		load_list = []
		load_list = fp.fout_posts()
		str_return = "facebook_parsing"
		for load in load_list:
			try:
				datas = parsing_data(load[0].decode('utf8'),load[1].decode('utf8'),load[2].decode('utf8'),load[3].decode('utf8'),load[4].decode('utf8'),load[5].decode('utf8'),load[6])
				db.session.add(datas)
				db.session.commit()
			except:
				pass
		return str_return
#	@classmethod
#	여기에 파싱데이터 넣으면 되겠다	
	"""
