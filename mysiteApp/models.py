# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

#角色
class Role(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    def __unicode__(self):
        return self.name

# 用户
class User(models.Model) :
    name = models.CharField('name', max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=30)
    role = models.ForeignKey(Role) #角色 多对一
    real_name = models.CharField('real_name', max_length=30, null=True, blank=True)
    weight = models.DecimalField('weight', max_digits=4, decimal_places=1, null=True, blank=True)
    height = models.DecimalField('height', max_digits=4, decimal_places=1, null=True, blank=True)
    sex = models.IntegerField('sex', null=True, blank=True) # 0-男，1-女
    birthday = models.DateField('birthday', null=True, blank=True)
    email = models.EmailField('email', null=True, blank=True)

    def __unicode__(self):
        return self.name

#令牌
class Token(models.Model):
    token = models.CharField('token', max_length=50, unique=True, db_index=True)
    user = models.OneToOneField(User) # 一对一
    expire = models.BigIntegerField('expire')

    def __unicode__(self):
        return self.token

#加速度
class Acceleration(models.Model) :
    user = models.ForeignKey(User) # 一对一
    device_id = models.CharField('device_id', max_length=30)
    timestamp = models.BigIntegerField('timetamp')
    x = models.DecimalField('x', max_digits=20, decimal_places=10)
    y = models.DecimalField('y', max_digits=20, decimal_places=10)
    z = models.DecimalField('z', max_digits=20, decimal_places=10)

# 角加速度
class AngleAcceleration(models.Model) :
    user = models.ForeignKey(User) # 一对一
    device_id = models.CharField('device_id', max_length=30)
    timestamp = models.BigIntegerField('timetamp')
    x = models.DecimalField('x', max_digits=20, decimal_places=10)
    y = models.DecimalField('y', max_digits=20, decimal_places=10)
    z = models.DecimalField('z', max_digits=20, decimal_places=10)

#压力
class Pressure(models.Model) :
    user = models.ForeignKey(User) # 一对一
    device_id = models.CharField('device_id', max_length=30)
    timestamp = models.BigIntegerField('timestamp')
    a = models.DecimalField('a', max_digits=20, decimal_places=10)
    b = models.DecimalField('b', max_digits=20, decimal_places=10)
    c = models.DecimalField('c', max_digits=20, decimal_places=10)
    d = models.DecimalField('d', max_digits=20, decimal_places=10)

# 信号强度
class Signal(models.Model):
    signal_strength = models.IntegerField('signal_strength')
    timestamp = models.BigIntegerField('timestamp')

# 每日步数
class Step(models.Model):
    user = models.ForeignKey(User)
    device_id = models.CharField('device_id', max_length=30)
    steps = models.IntegerField('steps')
    start_time = models.BigIntegerField('start_time')
    end_time = models.BigIntegerField('end_time')

# 实时步速
class Velocity(models.Model):
    user=models.ForeignKey(User)
    #user_name=models.CharField('user_name',max_length=30)
    device_id=models.CharField('device_id',max_length=30)
    velocity=models.FloatField('velocity')
    # timestamp=models.BigIntegerField('timestamp')
    distance=models.FloatField('distance')

#订阅
class Subscribe(models.Model):
    subscribe_from = models.ForeignKey(User, related_name="subscribe_from") # 一对多
    subscribe_to = models.ForeignKey(User, related_name="subscribe_to") # 一对多


    

