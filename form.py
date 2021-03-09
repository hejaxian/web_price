#coding=utf-8
#加载wtf表单模块
from flask import Flask
from flask_wtf import FlaskForm as Form
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError, Optional

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

#定义查询表单
class Query_price(Form):
	year = [('2004','2004'),('2005','2005'),
			('2006','2006'),('2007','2007'),('2008','2008'),
			('2009','2009'),('2010','2010'),('2011','2011'),
			('2012','2012'),('2013','2013'),('2014','2014'),
			('2015','2015'),('2016','2016'),('2017','2017'),
			('2018','2018'),('2019','2019'),('2020','2020'),
			('2021','2021')
	       ]
	month = [('1','1'),('2','2'),('3','3'),
			 ('4','4'),('5','5'),('6','6'),
			 ('7','7'),('8','8'),('9','9'),
			 ('10','10'),('11','11'),('12','12')]
	city_list = [('1','江门'),('2','新会'),('3','恩平'),('4','开平'),('5','台山')]
	
	name = StringField(u'材料名称',validators=[DataRequired(u'请输入材料名称')])
	size = StringField(u'规格',validators=[Optional()])
	city = SelectField(u'城市', choices=city_list)
	start_year = SelectField(u'起始年份', choices=year ,default='2019' )
	end_year = SelectField(u'结束年份', choices=year ,default='2019' )
	start_month = SelectField(u'起始月份', choices=month )
	end_month = SelectField(u'结束月份', choices=month )
	submit = SubmitField(u'查找') 
	
class Download_price(Form):
	year = [('2004','2004'),('2005','2005'),
			('2006','2006'),('2007','2007'),('2008','2008'),
			('2009','2009'),('2010','2010'),('2011','2011'),
			('2012','2012'),('2013','2013'),('2014','2014'),
			('2015','2015'),('2016','2016'),('2017','2017'),
			('2018','2018'),('2019','2019'),('2020','2020'),
	       		('2021','2021')
	       ]
	month = [('1','1'),('2','2'),('3','3'),
			 ('4','4'),('5','5'),('6','6'),
			 ('7','7'),('8','8'),('9','9'),
			 ('10','10'),('11','11'),('12','12')]
	city_list = [('1','江门'),('2','新会'),('3','恩平'),('4','开平'),('5','台山')]

	city = SelectField(u'城市', choices=city_list)
	download_year = SelectField(u'下载年份', choices=year, default='2019')
	download_month = SelectField(u'下载月份', choices=month )
	submit = SubmitField(u'下载')
