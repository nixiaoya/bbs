#coding=utf-8

from User.models import User
import re

class UserForm(object):
    def __init__(self,request):
        self.username = request.POST.get("username","").strip()
        self.password = request.POST.get("password","").strip()
        self.email = request.POST.get("email","").strip()
        self.signature = request.POST.get("signature","").strip()
        self.error = ""

    def clean_username(self):
        re1 = re.compile(r'[^\w\u4e00-\u9fa5]+')
        flag = False

        try:
            self.username = self.username.encode("utf-8")
        except UnicodeDecodeError:
            self.error = u"用户名编码错误"
        else:
            if self.username:
                if re1.match(self.username):
                    self.error = u"非法的用户名"
                else:
                    flag = True
            else:
                self.error = u"用户名不能为空"
        return flag

    def clean_password(self):
        re1 = re.compile(r'^[a-zA-Z0-9_]+$')
        flag = False
        if self.password:
            if re1.match(self.password):
                flag = True
            else:
                self.error = u"非法的密码"
        else:
            self.error = u"密码不能为空"
        return flag

    def clean_email(self):
        re1 = re.compile(r'^[a-zA-Z0-9_]{3,15}@[a-zA-Z0-9]{2,10}\.[a-z]{2,3}$')
        flag = False
        if self.email:
            if re1.match(self.email):
                flag = True
            else:
                self.error = u"非法的邮箱地址"
        else:
            self.error = u"邮箱不能为空"
        return flag

    def is_valid(self):
        key = True
        check_all = [
            self.clean_username(),
            self.clean_password(),
            self.clean_email(),
        ]

        for item in check_all:
            if not item:
                key = False
                break
        return key

    def save(self):
        user = User()
        user.username = self.username
        user.set_password(self.password)
        user.email = self.email
        if self.signature:
            user.signature = self.signature
        user.save()
        return user