# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django import forms
from mysiteApp.models import User, Role, Token, Subscribe, Acceleration, Pressure,Velocity

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



# 初始化Role表
def test_json(req):
    #将json数据转化为python数据格式
    data = simplejson.loads(req.body)

    # name = data['user']['name']
    # password = data['user']['password']
    #
    # #admin
    # #customer
    # customerRole = Role.objects.get(name='customer')
    #
    # user = User()
    # user.name = name
    # user.password = password
    # user.role = customerRole
    # user.save()
    customerRole = Role()
    customerRole.name = "admin"
    customerRole.save()

    customerRole1 = Role()
    customerRole1.name = "customer"
    customerRole1.save()

    result = {
        'successful': True
    }
    return HttpResponse(simplejson.dumps(result), content_type="application/json")

#注册
def signup(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #将提交的用户名保存在name变量中
        name = data['user']['name']
        #将提交的用户密码保存在password变量中
        password = data['user']['password']
        #将提交的用户角色保存在customerRole变量中
        customerRole = Role.objects.get(name='customer')
        #获取用户数据
        #以下为用户选填内容，故若用户填写则保存在变量之中，若字符串为空则变量中为None
        real_name = noneIfNoKey(data['user'], 'real_name')
        height = noneIfNoKey(data['user'], 'height')
        weight = noneIfNoKey(data['user'], 'weight')
        sex = noneIfNoKey(data['user'], 'sex')
        birthday = noneIfNoKey(data['user'], 'birthday')
        email = noneIfNoKey(data['user'], 'email')
        #创建一个空的User对象
        user = User()
       #将从json中获取的各种数据填入对象之中
        user.name = name
        user.password = password
        user.role = customerRole
        user.real_name = real_name
        user.height = height
        user.weight = weight
        user.sex = sex
        user.birthday = birthday
        user.email = email
        #将对象提交到数据库，保存更改
        user.save()
        #构建一个表示成功的dict
        result = {
            'successful': True,
            'error' : {
                'id' : '',
                'message' : ''
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
        #返回结果
        return HttpResponse(simplejson.dumps(result), content_type="application/json")



#login
def login(req):
    #获取日志
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #将提交的用户名保存在name变量中
        name = data['user']['name']
        #将提交的用户密码保存在password变量中
        password = data['user']['password']

        #登录名与密码出现错误
        customerUser=User()
        #根据用户名获取密码
        customerUser=User.objects.get(name = name)
        #判断密码是否正确
        if (password==customerUser.password):
            #密码正确则获取Token
            token=Token()
            token=Token.objects.filter(user=customerUser)
            #首次登陆token为空则删除
            if (len(token) != 0) :
                token.delete()
        else :
            #若密码不符则抛出异常
            raise myError('登录名与密码出现错误!')
        #生成随机字符串
        customerToken = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        #将信息写入token对象
        token = Token()
        token.token = customerToken
        token.user = customerUser
        token.expire = '-1'
        #将Token对象写入数据库
        token.save()
        #构建一个表示成功的dict，data中的token字段为生成的随机令牌
        result = {
            'data' : {
                'token':customerToken,
                #？？？？？
                'expire':-1
            },
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
    #捕获异常
    except myError as e:
        logger.error(e.value)
        #构建一个表示失败的dict
        result={
            'successful': False,
            'error' : {
                'id' : '1',
                'message' : e.value
            }
        }
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
        #将表示成功的dict以json返回到前段
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


#logout
def logout(req):
    #捕获异常
    logger=logging.getLogger('mysiteApp.views')
    try:
        #将json数据转化为python数据格式
        data = simplejson.loads(req.body)
        #获取用户令牌
        customerToken=data['token']
        token=Token()
        #依据用户令牌从数据库获取token
        token=Token.objects.get(token=customerToken)
        token.delete()
        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
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
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


#subscribe 关联用户
def subscribe(req):
    logger=logging.getLogger('mysiteApp.views')
    try:
        data = simplejson.loads(req.body)

        customerToken=data['token']
        customerName=data['user']['name']

        userFrom=User()
        token=Token.objects.get(token=customerToken)
        userFrom=token.user

        userTo=User()
        user=User()
        user=User.objects.get(name=customerName)
        userTo=user

        if (userFrom.id == userTo.id):
            raise myError('不允许关联自己')

        subscribe=Subscribe()
        subscribe.subscribe_from=userFrom
        subscribe.subscribe_to=userTo
        subscribe.save()

        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
    except myError as e:
        logger.error(e.value)
        result={
            'successful': False,
            'error' : {
                'id' : '2',
                'message' : e.value
            }
        }
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
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


#user/info
def info(req):
    logger=logging.getLogger('mysiteApp.views')
    try:
        data = simplejson.loads(req.body)

        token=Token()
        token=Token.objects.get(token=data['token'])
        customerUser=User()
        customerUser=token.user
        result = {
            'user':{
                "name" : customerUser.name,
                "password" : customerUser.password,
                "real_name" : customerUser.real_name,
                "height" : customerUser.height,
                "weight" : customerUser.weight,
                "sex" : customerUser.sex,
                "birthday" : str(customerUser.birthday),
                "email" : customerUser.email
            },
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
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
        return HttpResponse(simplejson.dumps(result), content_type="application/json")



#user/info/update
def info_update(req):
    logger=logging.getLogger('mysiteApp.views')
    try :
        data = simplejson.loads(req.body)
        user=User()
        token=Token()
        token=Token.objects.get(token=data['token'])
        user=token.user
        if 'real_name' in data['user']:
            user.real_name=noneIfEmptyString(data['user']['real_name'])
        if 'height' in data['user']:
            user.height=noneIfEmptyString(data['user']['height'])
        if 'weight' in data['user']:
            user.weight=noneIfEmptyString(data['user']['weight'])
        if 'sex' in data['user']:
            user.sex=noneIfEmptyString(data['user']['sex'])
        if 'birthday' in data['user']:
            user.birthday=noneIfEmptyString(data['user']['birthday'])
        if 'email' in data['user']:
            user.email=noneIfEmptyString(data['user']['email'])
        user.save()
        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
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
        return HttpResponse(simplejson.dumps(result), content_type="application/json")


#user/password/update
def password_update(req):
    logger=logging.getLogger('mysiteApp.views')
    try :
        data = simplejson.loads(req.body)

        user=User()
        token=Token()
        token=Token.objects.get(token=data['token'])
        user=token.user

        if (data['user']['old_password'] != user.password):
            raise myError('原密码输入错误！')

        user.password=data['user']['new_password']
        user.save()

        result = {
            'successful':True,
            'error':{
                'id':'',
                'message': ''
            }
        }
    except myError as e:
        logger.error(e.value)
        result={
            'successful': False,
            'error' : {
                'id' : '3',
                'message' : e.value
            }
        }
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
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

# 存储步速信息 result 来自于计算速度时的返回值
# def velocity(result):
#     logger=logging.getLogger('mysiteApp.views')
#     try:
#         data = simplejson.loads(req.body)
#         user = User()
#         token = Token()
#         token = Token.objects.get(token=data['token'])
#         user = token.user
#         d=Pressure().device_id
#         for tem in result:
#             v=Velocity(user=user,device_id=tem[0],velocity=tem[1],timestamp=tem[2])
#             v.save()
#     except Exception as e:
#         logger.error(e.args)
#     finally:
#         logger.disabled=True
    #Velocity.objects.create(device_id='abdc3eqw',velocity=1.11)

# 批量存储步速信息 result 来自于计算速度时的返回值
# def velocity(req):
#     logger=logging.getLogger('mysiteApp.views')
#
#     data = simplejson.loads(req.body)
#     user=User.objects.filter(name='1')
#     # user = User()
#     # token = Token()
#     # token = Token.objects.get(token=data['token'])
#     # user = token.user
#     d=Pressure.objects.filter(user).device_id[0]
#     velocitytemp = Velocity(user=user, device_id=d, velocity=1, distance=1)
#     velocitytemp.save()
#     # resultlist=[]
#     # for temp in result:
#     #      velocitytemp=Velocity(user=1,device_id=d,velocity=temp.velocity,distance=temp.distance)
#     #      resultlist.append(velocitytemp)
#     # Velocity.objects.dulk_create(resultlist)
#     return




