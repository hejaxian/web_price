# coding=utf-8
from flask import Flask, render_template, g, jsonify, request, Response, make_response, url_for, redirect, flash
# 加载bootstrap框架模块
from flask_bootstrap import Bootstrap
# 加载表单
from form import *
# 加载数据库
from sql import *

import tablib
import datetime
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)

# 定义日期格式
def datetimeformat(value, format="%Y-%m"):
    return value.strftime(format)


app.jinja_env.filters['datetimeformat'] = datetimeformat

# 配置返回JSON格式
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'
# 配置CSRF_key
app.config['SECRET_KEY'] = 'any string'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

# 全角半角转换表
table = {ord(f): ord(t) for f, t in zip(
    u'“”‘’，。！？【】（）％＃＠＆１２３４５６７８９０',
    u'\"\"\'\',.!?[]()%#@&1234567890')}


@app.route('/', methods=['POST', 'GET'])
def index():
    form = Query_price()
    if form.validate_on_submit():
        cityid = int(form.city.data)
        # 台山信息价按季度查询
        if cityid == 5:
            Str_date = datetime.datetime(int(form.start_year.data), int(form.start_month.data), 14, 00, 00, 00)
            End_date = datetime.datetime(int(form.end_year.data), int(form.end_month.data), 16, 00, 00, 00)
            # 其余区、市按月查询
        else:
            Str_date = datetime.datetime(int(form.start_year.data), int(form.start_month.data), 1, 00, 00, 00)
            End_date = datetime.datetime(int(form.end_year.data), int(form.end_month.data), 6, 00, 00, 00)

        city_list = [1, 2, 3, 4, 5]
        database_list = [JM_Price, XH_Price, EP_Price, KP_Price, TS_Price]
        cityid_index = city_list.index(cityid)
        Price = database_list[cityid_index]

        # 精确匹配材料名
        material_name = form.name.data
        material_name = material_name.translate(table)
        if re.match(r'"(.*)"', material_name):
            pattern = re.compile('"(.*)"')
            name = pattern.findall(material_name)
            Query = Price.select().where(Price.name == name).where(Price.issueDate.between(Str_date, End_date)).order_by(
                Price.issueDate)
        else:
            Query = Price.select().where(Price.name.contains(form.name.data)).where(
                Price.issueDate.between(Str_date, End_date)).order_by(Price.issueDate)

        delete_obj = Query
        size1 = None
        size2 = None
        size3 = None
        material_size = form.size.data
        material_size = material_size.translate(table)
        if re.match(r'(.*)\&(.*)', material_size):
            pattern = re.compile(r'(.*)\&(.*)')
            size = pattern.match(material_size)
            size1 = size.group(1)
            #尝试是否存在size2

            size2 = size.group(2)
            #如果size2存在!(size3),分离size3并自动查询size1&size2!size3
            if re.match(r'(.*)!(.*)', size2):
                pattern = re.compile('(.*)!(.*)')
                nosize = pattern.match(size2)
                size2 = nosize.group(1)
                size3 = nosize.group(2)
                delete = delete_obj.where(
                    Price.spec.contains(size3) & Price.spec.contains(size1) & Price.spec.contains(size2))
                delete_list = []
                for i in delete:
                    delete_list.append(i.spec)
                Query = Query.where(Price.spec.contains(size1) & Price.spec.contains(size2)).where(~(Price.spec << delete_list))
                #如果size2不存在!(size3),则查询size1&size2
            else:
                Query = Query.where(Price.spec.contains(size1) & Price.spec.contains(size2))

        #如果size1存在!(size3),则查询size1!size3
        elif re.match(r'(.*)!(.*)', material_size):

            pattern = re.compile('(.*)!(.*)')
            nosize = pattern.match(material_size)
            size1 = nosize.group(1)
            size3 = nosize.group(2)
            delete = delete_obj.where(
                    Price.spec.contains(size3) & Price.spec.contains(size1) )
            delete_list = []
            for i in delete:
                delete_list.append(i.spec)
            Query = Query.where(Price.spec.contains(size1)).where(~(Price.spec << delete_list))

        elif form.size.data == '':
            #如果材料名为空，直接跳过材料名的所有查询语句
            pass
        else:
            #一般情况下，对材料名进行模糊搜索
            Query = Query.where(Price.spec.contains(material_size))

        g.query = Query
        try:
            price = []
            notexprice = []
            for i in Query:
                price.append(i.price)
                notexprice.append(i.notaxPrice)
            g.avg = round(sum(price) / len(price), 2)
            g.notexavg = round(sum(notexprice) / len(notexprice), 2)
        except:
            flash(u'查询失败，请检查材料名称与规格')
        db.close()
    return render_template('index.html', form=form)


@app.route('/download_price', methods=['POST', 'GET'])
def download_price():
    form = Download_price()
    if form.validate_on_submit():
        year = form.download_year.data
        month = form.download_month.data
        cityid = form.city.data
        return redirect(url_for('output_excel', cityid=cityid, year=year, month=month))
    return render_template('download_price.html', form=form)


@app.route('/get_name/<int:cityid>')
def get_name(cityid):
    key = request.args.get('term')
    name_dict = {}
    name_list = []
    Query = Name_Index.select().where(Name_Index.name.contains(key) & (Name_Index.cityid == cityid))
    for i in Query:
        data = {"label": i.name, "value": i.name}
        if data not in name_list:
            name_list.append(data)
    return jsonify(name_list)


@app.route('/output_excel/<int:cityid>/<int:year>/<int:month>')
def output_excel(cityid, year, month):

    filename = str(year) + '-' + str(month) + '.xlsx'
    city_list = [1, 2, 3, 4, 5]
    database_list = [JM_Price, XH_Price, EP_Price, KP_Price, TS_Price]
    cityid_index = city_list.index(cityid)
    Price = database_list[cityid_index]

    Download_date_str = datetime.datetime(year, month, 1, 00, 00, 00)
    Download_date_end = datetime.datetime(year, month, 28, 00, 00, 00)

    Query = Price.select().where((Price.issueDate.between(Download_date_str, Download_date_end)))
    headers = ('材料名称', '规格', '单位', '价格', '不含税价', '折税率', '品牌', '备注')
    data = []
    for q in Query:
        name = q.name
        spec = q.spec
        unit = q.unit
        price = q.price
        notexprice = q.notaxPrice
        taxRate = q.taxRate
        if q.brand is None:
            brand = ''
        else:
            brand = q.brand

        if q.note is None:
            note = ''
        else:
            note = q.note
        data.append([name, spec, unit, price, notexprice, taxRate, brand, note])
    data = tablib.Dataset(*data, headers=headers)
    content = data.xlsx
    response = make_response(content)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
    db.close()
    return response


if __name__ == '__main__':
    app.run("0.0.0.0",debug=True,port=8000)
