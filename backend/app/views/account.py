from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *


class Login(APIView):
    def post(self, request):
        data = request.data
        print("login data:")
        print(data)  # debug
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin')
        value = 0
        debug = False
        if debug:
            all_user = User.objects.all()
            for user in all_user:
                print(user.username)
        try:
            item = User.objects.get(username=username)
            print("user")
            print(item)
        except Exception as e:
            print(e)
            value = 1
        # 用户存在
        if value == 0:
            if password != item.password or is_admin > item.is_admin:
                value = 2  # 密码错误或权限错误
            elif item.isBaned:
                value = 3
            else:
                # 成功登录
                request.session['username'] = username
        return Response({
            'value': value
        })
