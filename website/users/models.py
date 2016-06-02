#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string

import hashlib
import time

#------ 用户模块 -------

class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    passwd = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    signature = models.CharField(max_length=128,default='This guy is very lazy to leave anything here')
    photo = models.CharField(max_length=256, default="default.png")
    is_login = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    salt = models.CharField(max_length=256)
    token = models.CharField(max_length=64,blank=True)
    
    def genSalt(self):
        m1 = hashlib.md5()
        m1.update(str(time.time()))
        return m1.hexdigest()[:10]

    def e1(self,str_):
        m1 = hashlib.md5()
        m1.update(self.username + str_)
        return m1.hexdigest()

    def encrypt(self,str_):
        s1 = hashlib.sha256()
        s1.update(str_)
        return s1.hexdigest()

    def set_token(self):
        self.token = self.genSalt()
        self.save()

    def set_login(self):
        self.is_login = True
        self.save()

    def set_logout(self):
        self.is_login = False
        self.save()

    def set_active(self):
        self.active = True
        self.save()

    def set_password(self,str_):
        self.salt = self.genSalt()
        self.passwd = self.encrypt(self.e1(str_) + self.salt)
        self.save()

    def check_password(self,str_):
        return self.passwd == self.encrypt(self.e1(str_) + self.salt)

    def sendMail(self,msgType,host="172.16.36.39"):
        email_subject =""
        email_body =""
        self.set_token()

        if msgType == "register":
            email_subject = "Welcome join in Chouti"
            email_body = render_to_string("user/email_signup.txt",{"username":self.username,"token":self.token,"host":host})
        elif msgType == "reset":
            email_subject = "Reset your password for Chouti"
            email_body = render_to_string("user/email_reset.txt",{"username":self.username,"token":self.token,"host":host})
        send_mail(email_subject, email_body, 'P_cngb_db@genomics.cn',[self.email,], fail_silently=False)

    def __unicode__(self):
        return self.username

class Anonymouse(object):
    def __init__(self):
        self.username = ""
        self.passwd = ""
        self.is_login = False
        self.active = False

    def __unicode__(self):
        return "Anonymouse User"
