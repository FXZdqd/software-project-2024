from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account, question, follow, search, answer
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
    path('adminregister', account.AdminRegister.as_view()),
    path('resetUsername', account.UpdateUsername.as_view()),
    path('resetPassword', account.UpdatePassword.as_view()),
    path('getAllUser', account.GetAllUsers.as_view()),
    path('setAvatar', account.SetAvatar.as_view()),
    path('getAvatar', account.GetAvatar.as_view()),
    path('deleteUser', account.DeleteUser.as_view()),
    path('banUser', account.BanUser.as_view()),
    path('setUserInfo', account.SetUserInfo.as_view()),
    path('getUser', account.GetUser.as_view()),

    # 问题相关
    path('getAllQuestion', question.GetAllQuestions.as_view()),
    path('addQuestion', question.CreateQuestion.as_view()),
    path('delQuestion', question.DeleteQuestion.as_view()),
    path('chaQuestion', question.ChangeQuestion.as_view()),
    path('likeQuestion', question.LikeQuestion.as_view()),
    path('unlikeQuestion', question.UnlikeQuestion.as_view()),
    path('checkUserlikeQuestion', question.CheckUserLikeQuestion.as_view()),
    path('getQuestion', question.GetQuestion.as_view()),
    path('viewQuestion', question.ViewQuestion.as_view()),
    path('reportQuestion', question.ReportQuestion.as_view()),

    # 回答相关
    path('goAnswer', answer.CreateAnswer.as_view()),
    path('likeAnswer', answer.LikeAnswer.as_view()),
    path('unlikeAnswer', answer.UnlikeAnswer.as_view()),
    path('checkUserlikeAnswer', answer.CheckUserLikeAnswer.as_view()),
    path('reportAnswer', answer.ReportAnswer.as_view()),
    # 关注功能
    path('follow', follow.AddFollowQuestion.as_view()),
    path('unfollow',follow.UnfollowQuestion.as_view()),
    path('user_follow', follow.GetUserFollowedQuestions.as_view()),

    # 搜索功能
    path('getQuestionByTag', search.GetQuestionsByTag.as_view()),
    path('getQuestionByKeyword', search.GetQuestionByKeyword.as_view()),
    path('searchUser', search.SearchUser.as_view()),
    path('getQuestionAskedByUser', search.GetQuestionAskedByUser.as_view()),
    path('getQuestionAnsweredByUser', search.GetQuestionAnsweredByUser.as_view()),
    path('getAllUserByReport', search.GetAllUserByReport.as_view()),
    path('getAllQuestionByReport', search.GetAllQuestionByReport.as_view()),
    # path('getQuestionByTagUser', search.GetQuestionsByTagUser.as_view()),
    # path('getQuestionByKeywordUser', search.GetQuestionsByTagUser.as_view())
]
