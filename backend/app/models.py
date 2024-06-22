from django.db import models

NAME_LEN = 10  # tag
PASSWD_LEN = 20
PHONE_LEN = 15
QUESTION_LEN = 20

TAG_CHOICES = [
    ('course', '课程'),
    ('research', '科研'),
    ('further_study', '升学'),
    ('competition', '竞赛'),
    ('other', '其他'),
]


class Tag(models.Model):
    name = models.CharField(max_length=50, choices=TAG_CHOICES, unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=NAME_LEN)
    password = models.CharField(max_length=PASSWD_LEN)
    phone = models.CharField(max_length=PHONE_LEN + 1)
    is_admin = models.BooleanField(default=False)
    is_baned = models.BooleanField(default=False)
    new_field = models.CharField(max_length=100, default='default_value')  # 添加默认值
    optional_field = models.CharField(max_length=100, null=True)  # 允许为空
    reports = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, blank=True)  # 性别
    grade = models.CharField(max_length=10, blank=True)  # 年级
    department = models.CharField(max_length=100, blank=True)  # 院系


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    reports = models.IntegerField(default=0)


class Answer(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    likes = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)


class UserFollowedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class UserLikeQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')  # 确保每个用户对每个问题只有一条记录


class UserLikeAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')


class Avator(models.Model):
    file = models.ImageField(upload_to='avator/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
