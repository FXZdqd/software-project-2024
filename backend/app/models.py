from django.db import models

NAME_LEN = 10  # tag
PASSWD_LEN = 20
WECHAT_LEN = 30
PHONE_LEN = 15
QUESTION_LEN = 20


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=NAME_LEN, primary_key=True)
    password = models.CharField(max_length=PASSWD_LEN)
    is_admin = models.BooleanField(default=False)
    isBaned = models.BooleanField(default=False)
