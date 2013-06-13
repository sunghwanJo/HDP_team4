# -*- coding: utf-8 -*-
import urllib2

class cafe_parsing():

	def __init__(self):
		self.pf_list = ["이익훈", "강성훈","구승모", "김동진", "김종규","박재성","서경진","손영수","오동우","윤지수","이남영","임석현","정호영","조혜연","주형철","함석진","홍은택","김평철"]
		self.post_dic = {}
		self.comment_dic = {}

	def split_data(self):

		url = "http://cafe.nhnnext.org/"
		page = urllib2.urlopen(url)
		text = page.read().decode("utf8")

		s = text.encode('utf8')

		split_line = s.split('\n')

		data_mode = "post"
		reading_mode = False

		temp_txt = ""

		for line in split_line:
			line = line.replace("\t","")

			if "<td class=\"title\">" in line:
				reading_mode = True
			if reading_mode == True:
				line = line.replace("\n","")
				line = line.replace("\r","")
				temp_txt += line
			

			if "<h3 class=\"widgetBoxHeader\">카페 최신 댓글</h3>" in line:
				data_mode = "comment"

			if "<td class=\"title\">" in line:
				reading_mode = True
				num=0
			

			if "</tr><tr>" in line:
				reading_mode = False
				temp_txt = temp_txt.replace("<strong>","``")
				temp_txt = temp_txt.replace("</strong>","``")

				temp_txt = temp_txt.replace("<a href=\"","``")
				temp_txt = temp_txt.replace("\">","``")
				
				
				temp_txt = temp_txt.replace(" <span class=\"icon","``")
				
				temp_txt = temp_txt.replace("</span></td>","``")
				temp_txt = temp_txt.replace("<td>","``")
				temp_txt = temp_txt.replace("</td></tr><tr>","``")

				#print dic_key[0]
				if data_mode == "post":
					split_temp = []
					split_temp = temp_txt.split("``")
					self.post_dic[split_temp[10]] = split_temp
					temp_txt = ""
				else:
					#comment_dic[dic_key[0]] = parse_temp
					split_temp = []
					temp_txt = temp_txt.replace("</a>","``")
					split_temp = temp_txt.split("``")
					self.comment_dic[split_temp[12]] = split_temp
					temp_txt = ""


	def fout_post(self):
		#@app.route('/db_commit/<url>/<site>/<location>/<title>/<datetime>/<username>/<category>')
		data_list = []
		category = u""
		#학생들이 과제를 올리는 과제게시판도 있어 교수님이 올린 경우만 과제로 저장
		for data in self.post_dic :

			if ( (("과제" in self.post_dic[data][8]) or ("과제" in self.post_dic[data][11])) and (self.post_dic[data][17] in self.pf_list) ) :	
				category = u"과제"

			#공지 게시판에 올라간 글을 공지로 저장
			elif ( ("공지" in self.post_dic[data][8]) or ("notice" in self.post_dic[data][8]) ) :	
				category = u"공지"
			
			elif ( ("택배" in self.post_dic[data][8]) ):
				category = u"택배"
			

			#그 외 글은 기타로 저장
			else :
				category = u"기타"	
			data_list.append([self.post_dic[data][10],"cafe",self.post_dic[data][4]+" - "+self.post_dic[data][8],self.post_dic[data][11],self.post_dic[data][15],self.post_dic[data][17],category])
			#url,site,location,title,datetime,username,category
		return data_list
		#for data in self.post_dic :	
		#	return (self.post_dic[data][10],"cafe",self.post_dic[data][4] + " - " + self.post_dic[data][8],self.post_dic[data][15],self.post_dic[data][17],category)
		"""
		f = open('../fout.txt', 'w')
		for data in self.post_dic :					#$로 구분
			f.write(self.post_dic[data][10] + "$")	#URL
			f.write("cafe")							#대분류	
			f.write(self.post_dic[data][4] + " - " +
					self.post_dic[data][8] + "$" )	#까페 이름 + 게시판 이름
			f.write(self.post_dic[data][11] + "$")	#게시글 제목
			f.write(self.post_dic[data][15] + "$")	#작성시간
			f.write(self.post_dic[data][17] + "$")	#작성자
			
			#학생들이 과제를 올리는 과제게시판도 있어 교수님이 올린 경우만 과제로 저장
			if ( (("과제" in self.post_dic[data][8]) or ("과제" in self.post_dic[data][11])) and (self.post_dic[data][17] in self.pf_list) ) :	
				f.write("과제"+"\n")
			
			#공지 게시판에 올라간 글을 공지로 저장
			elif ( ("공지" in self.post_dic[data][8]) or ("notice" in self.post_dic[data][8]) ) :	
	 			f.write("공지"+"\n")
	 		
	 		#그 외 글은 기타로 저장
	 		else :
	 			f.write("기타"+"\n")		
	 	"""			

"""
# Test Code
cp = cafe_parsing()
cp.split_data()
cp.fout_post()
"""
