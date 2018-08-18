# -*- coding: utf-8 -*-
__author__ = 'Jianming'
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django import forms
from mysiteApp.models import User, Role, Token, Subscribe, Acceleration, Pressure, Signal, AngleAcceleration
from django.http.response import HttpResponseRedirect
from django.db import connection
import simplejson
import random
import string
import logging
import django.utils.log
import logging.handlers

# Create your views here.
##################### def ############################
#如果字符串为空，返回None
def noneIfEmptyString(value):
    if value == "":
        return None
    return value
#如果dict键值为空，返回None
def noneIfNoKey(dict, key):
    if key in dict:
        value = dict[key]
        if value == "":
            return None
        return value

    return None
#自定义错误类
class myError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
#########################################################
#所有返回结果中均存在successful字段，操作成功则successful字段为True，否则为False
#若有故障，则error中的message字段为报错信息
#data/upload
def data_upload(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #通过令牌从数据库获取用户
        token=Token()
        token=Token.objects.get(token=data['token'])
        user=User()
        user=token.user

        if ('signal' in data['data']):
            #创建空的singles list，
            signals = []
            #从data中获取一系列singal中的数据
            for tmp in data['data']['signal']:
                #创建一个model中的Single对象
                signal = Signal()
                #将signal数据写入
                signal.signal_strength=tmp['signal_strength']
                #将时间戳写入
                signal.timestamp=tmp['timestamp']
                #将这个对象追加到singles list中
                signals.append(signal)
                #批量创建对象，导入大量数据，提升性能，避免逐条插入
            Signal.objects.bulk_create(signals)

        if ('pressure' in data['data']):
            #创建空的pressures list
            pressures = []
            #从data中获取一系列pressures中的数据
            for tmp in data['data']['pressure']:
                #创建一个model中的pressures对象
                pressure = Pressure()
                #将user数据写入，对应每个用户的压力
                pressure.user=user
                #将device_id数据写入，对应每个设备的id
                pressure.device_id=data['device_id']
                #将时间戳写入
                pressure.timestamp=tmp['timestamp']
                #将不同pressure传感器的数据写入
                pressure.a=float(tmp['a'])
                pressure.b=float(tmp['b'])
                pressure.c=float(tmp['c'])
                pressure.d=float(tmp['d'])
                #将这个对象追加到pressures list中
                pressures.append(pressure)
            #批量创建对象，导入大量数据，提升性能，避免逐条插入
            Pressure.objects.bulk_create(pressures)

        if ('acceleration' in data['data']):
            #创建空的accelerations list
            accelerations = []
            #从data中获取一系列acceleration中的数据
            for tmp in data['data']['acceleration']:
                #创建一个model中的Acceleration对象
                acceleration=Acceleration()
                #将user数据写入，对应每个用户的Acceleration
                acceleration.user=user
                #将device_id数据写入，对应每个设备的id
                acceleration.device_id=data['device_id']
                #将时间戳写入
                acceleration.timestamp=tmp['timestamp']
                #将不同acceleration传感器的数据写入
                acceleration.x=float(tmp['x'])
                acceleration.y=float(tmp['y'])
                acceleration.z=float(tmp['z'])
                #将这个对象追加到acceleration list中
                accelerations.append(acceleration)
            #批量创建对象，导入大量数据，提升性能，避免逐条插入    
            Acceleration.objects.bulk_create(accelerations)
        
        if ('angleAcceleration' in data['data']):
            #创建空的angleAcceleration list
            angleAccelerations = []
            #从data中获取一系列angleAcceleration中的数据
            for tmp in data['data']['angleAcceleration'] :
                #创建一个model中的angleAcceleration对象
                angleAcceleration = AngleAcceleration()
                #将user数据写入，对应每个用户的angleAcceleration
                angleAcceleration.user = user
                #将device_id数据写入，对应每个设备的id
                angleAcceleration.device_id = data['device_id']
                #将时间戳写入
                angleAcceleration.timestamp = tmp['timestamp']
                #将不同angleAcceleration传感器的数据写入
                angleAcceleration.x = float(tmp['x'])
                angleAcceleration.y = float(tmp['y'])
                angleAcceleration.z = float(tmp['z'])
                #将这个对象追加到angleAcceleration list中
                angleAccelerations.append(angleAcceleration)
                #批量创建对象，导入大量数据，提升性能，避免逐条插入
            AngleAcceleration.objects.bulk_create(angleAccelerations)
        #构建一个表示成功的dict
        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
        #将表示成功的dict以json返回到前段
        #return HttpResponse(simplejson.dumps(result), content_type="application/json")
    #捕获异常
    except Exception as e:
        logger.error(e.args)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

def daily_data_upload(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #通过令牌从数据库获取用户
        token=Token()
        token=Token.objects.get(token=data['token'])
        user=User()
        user=token.user

        if ('steps' in data['data']):
            #创建空的singles list，
            stepslist = []
            #从data中获取一系列singal中的数据
            for tmp in data['data']['signal']:
                #创建一个model中的Single对象
                steps = Steps()
                #将signal数据写入
                steps.steps=tmp['steps']
                #将时间戳写入
                steps.timestamp=tmp['timestamp']
                #将这个对象追加到singles list中
                tepslist.append(signal)
                #批量创建对象，导入大量数据，提升性能，避免逐条插入
            Signal.objects.bulk_create(signals)

        #构建一个表示成功的dict
        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
        #将表示成功的dict以json返回到前段
        #return HttpResponse(simplejson.dumps(result), content_type="application/json")
    #捕获异常
    except Exception as e:
        logger.error(e.args)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


#数据库查询
def data_query(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #通过令牌从数据库获取用户
        token=Token()
        token=Token.objects.get(token=data['token'])
        user=User()
        user=token.user

        #创建一个model中的pressures对象
        pressure=Pressure()
        #获取该对象的迭代器，筛选条件为特定用户
        pressure=Pressure.objects.filter(user=user)
        #创建一个空的pressureList
        pressureList=[]
        #从迭代器中循环获取每一条记录的数据
        for tmp in  pressure:
            #将获取的数据组成一个dict追加到pressureList中
            pressureList.append({'a':tmp.a, 'b':tmp.b, 'c':tmp.c, 'd':tmp.d})
        #创建一个model中的Acceleration对象
        acceleration=Acceleration()
        #获取该对象的迭代器
        acceleration=Acceleration.objects.filter(user=user)
        #创建一个空的accelerationList
        accelerationList=[]
        #从迭代器中循环获取每一条记录的数据
        for tmp in acceleration:
            #将获取的数据组成一个dict追加到accelerationList中
            accelerationList.append({'x':tmp.x, 'y':tmp.y, 'z':tmp.z})
        #创建一个model中的AngleAcceleration对象      
        angleAcceleration = AngleAcceleration()
        #获取该对象的迭代器
        angleAcceleration = AngleAcceleration.objects.filter(user = user)
        #创建一个空的angleAccelerationList
        angleAccelerationList = []
        #从迭代器中循环获取每一条记录的数据
        for tmp in angleAcceleration :
            #将获取的数据组成一个dict追加到accelerationList中
            angleAccelerationList.append({'x':tmp.x, 'y':tmp.y, 'z':tmp.z})
        #构建一个表示成功的dict，data中的pressures，accelerations，angleAccelerationList为查询结果
        result = {
            'successful':True,
            'data':{
                'pressures':pressureList,
                'accelerations':accelerationList,
                'angleAccelerations':angleAccelerationList,
                'id':'',
                'message': ''
            }
        }
    #捕获异常
    except Exception as e:
        logger.error(e.args)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        #返回结果
        logger.disabled=True
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# query pressure by time
def data_pressures_query(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #获取一个Pressure对象的迭代器，筛选条件为从data中获取的start_time到end_time
        pressures = Pressure.objects.filter(timestamp__gte = data['filter']['start_time'],
                                               timestamp__lte = data['filter']['end_time'])
        #创建一个空的pressuresList
        pressuresList = []
        #从迭代器中循环获取每一条记录的数据
        for tmp in pressures :
            #将获取的数据组成一个dict追加到pressureList中
            pressuresList.append({"timestamp":tmp.timestamp, "a":tmp.a, "b":tmp.b, "c":tmp.c, "d":tmp.d})
        #构建一个表示成功的dict，data中的pressures字段为查询结果
        result = {
            'successful':True,
            'data':{
                "pressures": pressuresList,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


# query acceleration by time
def data_acceleration_query(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #获取一个Acceleration对象的迭代器，筛选条件为从data中获取的start_time到end_time
        acceleration = Acceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])
        #创建一个空的accelerationList
        accelerationList = []
        #从迭代器中循环获取每一条记录的数据
        for tmp in acceleration :
            #将获取的数据组成一个dict追加到accelerationList中
            accelerationList.append({"timestamp":tmp.timestamp, "x":tmp.x, "y":tmp.y, "z":tmp.z})
        #构建一个表示成功的dict，data中的accelerations字段为查询结果
        result = {
            'successful':True,
            'data':{
                "accelerations": accelerationList,
            }
        }

    #捕获异常
    except Exception as e:
        logger.error(e.args)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# query angleAcceleration by time
def data_angleAcceleration_query(req) :
    #获取日志
    logger = logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #获取一个angleAcceleration对象的迭代器，筛选条件为从data中获取的start_time到end_time
        angleAcceleration = AngleAcceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])
        #创建一个空的angleAccelerationList
        angleAccelerationList = []
        #从迭代器中循环获取每一条记录的数据
        for tmp in angleAcceleration :
            #将获取的数据组成一个dict追加到accelerationList中
            angleAccelerationList.append({"timestamp":tmp.timestamp, "x":tmp.x, "y":tmp.y, "z":tmp.z})
        #构建一个表示成功的dict，data中的angleAcceleration字段为查询结果
        result = {
            'successful':True,
            'data':{
                "angleAcceleration": angleAccelerationList,
            }
        }

    #捕获异常
    except Exception as e:
        logger.error(e.args)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# step !!!没用上
# query steps by time
def data_steps_query(req):
    # 获取日志
    logger = logging.getLogger('mysiteApp.views')
    try:
        # 将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        # 获取一个Pressure对象的迭代器，筛选条件为从data中获取的start_time到end_time
        pressures = Pressure.objects.filter(timestamp__gte=data['filter']['start_time'],
                                            timestamp__lte=data['filter']['end_time'])
        # 创建一个空的pressuresList
        pressuresList = []
        # 从迭代器中循环获取每一条记录的数据
        for tmp in pressures:
            # 将获取的数据组成一个dict追加到pressureList中
            pressuresList.append({"timestamp": tmp.timestamp, "a": tmp.a, "b": tmp.b, "c": tmp.c, "d": tmp.d})
        # 构建一个表示成功的dict，data中的pressures字段为查询结果
        result = {
            'successful': True,
            'data': {
                "pressures": pressuresList,
            }
        }

    # 捕获异常
    except Exception as e:
        # 构建一个表示失败的dict
        logger.error(e.args)
        result = {
            'successful': False,
            'error': {
                'id': '1024',
                'message': e.args
            }
        }
    finally:
        logger.disabled = True
        # 以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


# query signal by time
def data_signal_query(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #获取一个Signal对象的迭代器，筛选条件为从data中获取的start_time到end_time
        signal = Signal.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])
        #创建一个空的angleAccelerationList
        signalList = []
        #从迭代器中循环获取每一条记录的数据
        for tmp in signal :
            #将获取的数据组成一个dict追加到accelerationList中
            signalList.append({"timestamp":tmp.timestamp, "signal_strength":tmp.signal_strength})
        #构建一个表示成功的dict，data中的signals字段为查询结果
        result = {
            'successful':True,
            'data':{
                "signals": signalList,
            }
        }

    #构建一个表示失败的dict
    except Exception as e:
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '1024',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

def data_pressures_count(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        pressurescount = Pressure.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time']).count()
        result = {
            'successful':True,
            'data':{
                #total为计算出的总页数
                "total_count": pressurescount,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

def data_acceleration_count(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        accelerationcount = Acceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time']).count()
        result = {
            'successful':True,
            'data':{
                "total_count": accelerationcount,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

def data_angleAcceleration_count(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        angleAccelerationcount = AngleAcceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time']).count()
        if angleAccelerationcount % page_size == 0:
            total_page = angleAccelerationcount/page_size
        else:
            total_page = angleAccelerationcount/page_size + 1
        result = {
            'successful':True,
            'data':{
                "total_page": total_page,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# step
def data_steps_count(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        pressurescount = Pressure.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time']).count()
        result = {
            'successful':True,
            'data':{
                #total为计算出的总页数
                "total_count": pressurescount,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")




def data_signal_count(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        signalcount = Signal.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time']).count()
        if signalcount % page_size == 0:
            total_page = signalcount/page_size
        else:
            total_page = signalcount/page_size + 1
        result = {
            'successful':True,
            'data':{
                "total_page": total_page,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# query pressure by time and paging
def data_pressures_query_pages(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的number(当前页码，0基址)
        page_number = data['page']['number']
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        beg = page_size * page_number
        #计算每页记录的结束位置
        end = page_size * (page_number + 1)
        #创建一个空的pressuresList
        pressuresList = []
        #从迭代器中循环获取每一条记录的数据，记录由beg和end切分
        #利用了querysets的惰性，后面的切片语句会转换为sql语句执行，提高查询效率
        pressures = Pressure.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])[beg:end]

        for tmp in pressures :
            #将获取的数据组成一个dict追加到pressureList中
            pressuresList.append({"timestamp":tmp.timestamp, "a":tmp.a, "b":tmp.b, "c":tmp.c, "d":tmp.d})
        #构建一个表示成功的dict，data中的pressures字段为查询结果
        result = {
            'successful':True,
            'data':{
                "pressures": pressuresList,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# query acceleration by time and paging
def data_acceleration_query_pages(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        page_number = data['page']['number']
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        beg = page_size * page_number
        #计算每页记录的结束位置
        end = page_size * (page_number + 1)
        #创建一个空的accelerationList
        accelerationList = []
        #从迭代器中循环获取每一条记录的数据，记录由beg和end切分
        acceleration = Acceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])[beg:end]
        #从迭代器中循环获取每一条记录的数据
        for tmp in acceleration :
            #将获取的数据组成一个dict追加到accelerationList中
            accelerationList.append({"timestamp":tmp.timestamp, "x":tmp.x, "y":tmp.y, "z":tmp.z})
        #构建一个表示成功的dict，data中的acceleration字段为查询结果
        result = {
            'successful':True,
            'data':{
                "accelerations": accelerationList,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# query angleAcceleration by time and paging
def data_angleAcceleration_query_pages(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的number(当前页码，0基址)
        page_number = data['page']['number']
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        beg = page_size * page_number
        #计算每页记录的结束位置
        end = page_size * (page_number + 1)
        #创建一个空的angleAccelerationList
        angleAccelerationList = []
        angleAcceleration = AngleAcceleration.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])[beg:end]
        #从迭代器中循环获取每一条记录的数据
        for tmp in angleAcceleration :
            #将获取的数据组成一个dict追加到angleAccelerationList中
            angleAccelerationList.append({"timestamp":tmp.timestamp, "x":tmp.x, "y":tmp.y, "z":tmp.z})
        #构建一个表示成功的dict，data中的angleAcceleration字段为查询结果
        result = {
            'successful':True,
            'data':{
                "angleAcceleration": angleAccelerationList,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# step
def data_steps_query_pages(req):
    # 获取日志
    logger = logging.getLogger('mysiteApp.views')
    try:
        # 将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        # 从json获取page对象中的number(当前页码，0基址)
        page_number = data['page']['number']
        # 从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        # 计算每页记录的起始位置
        beg = page_size * page_number
        # 计算每页记录的结束位置
        end = page_size * (page_number + 1)
        # 创建一个空的pressuresList
        pressuresList = []
        # 从迭代器中循环获取每一条记录的数据，记录由beg和end切分
        # 利用了querysets的惰性，后面的切片语句会转换为sql语句执行，提高查询效率
        pressures = Pressure.objects.filter(timestamp__gte=data['filter']['start_time'],
                                            timestamp__lte=data['filter']['end_time'])


        # def initT():
        #     global T, begin, end, finish, steps
        #     S = str(begin)
        #     f.write(S)
        #
        # # 步数统计
        # def count(a, T, size):
        #     global steps, n, peakFlag, NT


        # T = 0
        # NT = 0
        # begin = False
        # end = False
        # finish = False
        # peakFlag = False
        # n = 0
        flag = False
        steps = 0
        threshold = 20

        for tmp in pressures:
            a = int(tmp.a)


            if a < threshold and flag is False:
                flag = True
            elif a >= threshold and flag is True:
                steps += 1

                flag = False

            # if finish is False:
            #     if a < threshold and begin is False:
            #         begin = True
            #     elif a >= threshold and begin is True and end is False:
            #         T += 1
            #     if a < threshold and T != 0:
            #         T += 1
            #         end = True
            #     if a >= threshold and end is True:
            #         begin = False
            #         end = False
            #         finish = True
            #         steps += 1
            #
            #
            # else:
            #     size = T / 10
            #     if n == int(size):
            #         if peakFlag is False and a < threshold:
            #             peakFlag = True
            #         elif peakFlag is True and a >= threshold:
            #             peakFlag = False
            #             steps += 1
            #             T = int(NT)
            #             NT = 0
            #             n = 0
            #         NT += size
            #         if NT >= 5 * T:
            #             T = 0
            #             finish = False
            #         n = 0
            #     n += 1

        # 将获取的数据组成一个dict追加到pressureList中
        pressuresList.append({"start_time": data['filter']['start_time'], "end_time": data['filter']['end_time'], "steps": steps})
        # 构建一个表示成功的dict，data中的pressures字段为查询结果
        result = {
            'successful': True,
            'data': {
                "pressures": pressuresList,
            }
        }

    # 捕获异常
    except Exception as e:
        # 构建一个表示失败的dict
        logger.error(e.args)
        result = {
            'successful': False,
            'error': {
                'id': '',
                'message': e.args
            }
        }
    finally:
        logger.disabled = True
        # 以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


# query signal by time and paging
def data_signal_query_pages(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #从json获取page对象中的number(当前页码，0基址)
        page_number = data['page']['number']
        #从json获取page对象中的page_size(每页记录行数)
        page_size = data['page']['page_size']
        #计算每页记录的起始位置
        beg = page_size * page_number
        #计算每页记录的结束位置
        end = page_size * (page_number + 1)
        #创建一个空的signalList
        signalList = []
        signal = Signal.objects.filter(timestamp__gte = data['filter']['start_time'],
                                                timestamp__lte = data['filter']['end_time'])[beg:end]
        #从迭代器中循环获取每一条记录的数据
        for tmp in signal :
            #将获取的数据组成一个dict追加到signalList中
            signalList.append({"timestamp":tmp.timestamp, "signal_strength":tmp.signal_strength})
        #构建一个表示成功的dict，data中的signal字段为查询结果
        result = {
            'successful':True,
            'data':{
                "signal": signalList,
            }
        }

    #捕获异常
    except Exception as e:
        #构建一个表示失败的dict
        logger.error(e.args)
        result={
            'successful': False,
            'error' : {
                'id' : '',
                'message' : e.args
            }
        }
    finally:
        logger.disabled=True
        #以json的形式返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")
