from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account, question, follow
from app.views import view_set
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
# /user/由UserViewSet去处理
router.register(prefix='user', viewset=view_set.UserViewSet)

urlpatterns = [
    # 用户账户相关
    path('login', account.Login.as_view()),
    path('register', account.Register.as_view()),
    path('resetUsername', account.UpdateUsername.as_view()),
    path('resetPassword', account.UpdatePassword.as_view()),
    path('getAllUser', account.GetAllUsers.as_view()),

    # 问题相关
    path('getQuestion', question.GetQuestion.as_view()),
    path('getAllQuestion', question.GetAllQuestions.as_view()),
    path('addQuestion', question.CreateQuestion.as_view()),
    path('delQuestion', question.DeleteQuestion.as_view()),
    path('chaQuestion', question.ChangeQuestion.as_view()),

    # 关注功能
    path('follow', follow.FollowedQuestion.as_view()),
    path('user_follow', follow.GetUserFollowedQuestions.as_view())

]
