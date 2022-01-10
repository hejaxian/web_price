#coding=utf-8
#使用peewee 数据库ORM
from peewee import *
from playhouse.pool import PooledMySQLDatabase

#数据库
db = PooledMySQLDatabase('MYSQL_DATABASE',host='MYSQL_HOST',port='MYSQL_PORT',passwd='MYSQL_PASSWD',user='MYSQL_USER',charset='utf8mb4', max_connections=128,stale_timeout=300)

#定义模型
class BaseModel(Model):
    class Meta:
        database = db

class JM_Price(BaseModel):
    id = IntegerField()
    #材料分类
    specclass = CharField(null=True)
    #材料小类
    subclass = CharField(null=True)
    #名称
    name = CharField()
    #规格
    spec = CharField(null=True)
    #单位
    unit = CharField(null=True)
    #品牌
    brand = CharField(null=True)
    #价格（含税）
    price = FloatField()
    #除税价格
    notaxPrice = FloatField()
    #税率
    taxRate = FloatField()
    #备注
    note = CharField(null=True)
    #城市
    cityid = IntegerField()
    #时间
    issueDate = DateField()
    #journalId
    journalId = IntegerField()

class XH_Price(BaseModel):
    id = IntegerField()
    # 材料分类
    specclass = CharField(null=True)
    # 材料小类
    subclass = CharField(null=True)
    # 名称
    name = CharField()
    # 规格
    spec = CharField(null=True)
    # 单位
    unit = CharField(null=True)
    # 品牌
    brand = CharField(null=True)
    # 价格（含税）
    price = FloatField()
    # 除税价格
    notaxPrice = FloatField()
    # 税率
    taxRate = FloatField()
    # 备注
    note = CharField(null=True)
    # 城市
    cityid = IntegerField()
    # 时间
    issueDate = DateField()
    # journalId
    journalId = IntegerField()

class EP_Price(BaseModel):
    id = IntegerField()
    #材料分类
    specclass = CharField(null=True)
    #材料小类
    subclass = CharField(null=True)
    #名称
    name = CharField()
    #规格
    spec = CharField(null=True)
    #单位
    unit = CharField(null=True)
    #品牌
    brand = CharField(null=True)
    #价格（含税）
    price = FloatField()
    #除税价格
    notaxPrice = FloatField()
    #税率
    taxRate = FloatField()
    #备注
    note = CharField(null=True)
    #城市
    cityid = IntegerField()
    #时间
    issueDate = DateField()
    #journalId
    journalId = IntegerField()

class KP_Price(BaseModel):
    id = IntegerField()
    #材料分类
    specclass = CharField(null=True)
    #材料小类
    subclass = CharField(null=True)
    #名称
    name = CharField()
    #规格
    spec = CharField(null=True)
    #单位
    unit = CharField(null=True)
    #品牌
    brand = CharField(null=True)
    #价格（含税）
    price = FloatField()
    #除税价格
    notaxPrice = FloatField()
    #税率
    taxRate = FloatField()
    #备注
    note = CharField(null=True)
    #城市
    cityid = IntegerField()
    #时间
    issueDate = DateField()
    #journalId
    journalId = IntegerField()

class TS_Price(BaseModel):
    id = IntegerField()
    #材料分类
    specclass = CharField(null=True)
    #材料小类
    subclass = CharField(null=True)
    #名称
    name = CharField()
    #规格
    spec = CharField(null=True)
    #单位
    unit = CharField(null=True)
    #品牌
    brand = CharField(null=True)
    #价格（含税）
    price = FloatField()
    #除税价格
    notaxPrice = FloatField()
    #税率
    taxRate = FloatField()
    #备注
    note = CharField(null=True)
    #城市
    cityid = IntegerField()
    #时间
    issueDate = DateField()
    #journalId
    journalId = IntegerField()

class Name_Index(BaseModel):
    name = CharField()
    cityid = IntegerField()
