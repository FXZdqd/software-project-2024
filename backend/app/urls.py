from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account
from app.views import view_set
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
# /user/由UserViewSet去处理
router.register(prefix='user', viewset=view_set.UserViewSet)

urlpatterns = [
    path('login/', account.Login.as_view()),
]
