from django.db import models

NAME_LEN = 10  # tag
PASSWD_LEN = 20
PHONE_LEN = 15
QUESTION_LEN = 20


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=NAME_LEN, primary_key=True)
    password = models.CharField(max_length=PASSWD_LEN)
    phone = models.CharField(max_length=PHONE_LEN + 1)
    is_admin = models.BooleanField(default=False)
    is_baned = models.BooleanField(default=False)


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Answer(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class FollowedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='followers')
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # 确保用户不会重复关注同一个问题
