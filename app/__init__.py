# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
from app.cafe.cafe_parsing2 import *
from app.facebook.loader import *

import os
import json

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/')
def index_view():
	if 'name' in session:
		return redirect(url_for('board'))
	
	return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if 'name' in session:
		return redirect(url_for('board'))

	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']
		if user.query.filter_by(name=name,password=password).first():
			session['name'] = name
			return redirect(url_for("board"))
		else :
			return render_template("login.html", error_message='login_error')

	return render_template("login.html")
	
@app.route('/logout', methods=['POST', 'GET'])
def logout():
	session.pop('name')
	return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']
		password2 = request.form['password2']
		if not password == password2:
			return render_template('register.html', error_message=u'비밀번호를 확인해 주세요')
		try:
			db.session.add(user(name, password))
			db.session.commit()
		except:
			return render_template('register.html', error_message=u'중복임')
		return redirect(url_for("board"))

	return render_template('register.html')

@app.route('/selectcard', methods=['POST', 'GET'])
def selectcard() :
	if request.method == 'POST':
		
		result_str = ''
		for key in request.form.keys():
			result_str = result_str + request.form[key]	+ ':'
			
		result_str = result_str[:-1]

		human = user.query.filter_by(name=session['name']).first()
		human.category = result_str
		db.session.commit()
		
		return redirect(url_for('board'))

	return render_template("select_card.html")

@app.route('/board')
def board():
	class_set = {u'선생님글':'icon-users', u'교수님글':'icon-fork',  u'택배':'icon-truck', u'공지':'icon-megaphone', u'과제':'icon-pencil', u'기타':'icon-dot-3'}

	if 'name' in session:
		try:
			category_data = user.query.filter_by(name=session['name']).first().category.split(':')
		except:
			return redirect(url_for('selectcard'))
		
		result_dic = {}
		for category in category_data:
			result_dic[category] = parsing_data.query.filter_by(category=category).all()
		
		return render_template('board.html', username=session['name'], category_data=category_data, class_set=class_set, result_dic=result_dic)

	return redirect(url_for('login'))

@app.route('/getdata', methods=['POST', 'GET'])
def getdata():
	if request.method == 'POST' or True:
		category = request.args.get('category')
		db_data = parsing_data.query.filter_by(category=category).all()
		
		result_data = {}

		for idx, data in enumerate(db_data):
			result_data[str(idx)] = {'id':data.id, 'location':data.location, 'title':data.title, 'site':data.site, 'url':data.url}

		return json.dumps(result_data)

	return 'NULL'

class user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30),unique = True)
	password = db.Column(db.String(30))
	category = db.Column(db.String(50))


	def __init__(self, name, password):
		self.name = name
		self.password = password

class parsing_data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(250))			#게시글의 url address
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
	
	def __repr__(self):
		return '%s' %self.url

	def db_insert(self,url,site,location,title,datetime,username,category):
		data = parsing_data(url,site,location,title,datetime,username,category)
		db.session.add(data)
		db.session.commit()
		return "@@"
	
	@classmethod	
	def db_insert_facebook(cls):
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
	
	@classmethod
	def db_insert_cafe(cls):
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

