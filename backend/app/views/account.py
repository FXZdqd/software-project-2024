from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *
def check_username(username):
    value = 0
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        value = 1
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            value = 2
    return value == 2

class Register(APIView):
    def post(self, request):
        data = request.data
        phone = data.get('phone')
        name = str(data.get('username'))
        password = str(data.get('password'))
        password_re = str(data.get('password_re'))
        if not check_username(name):
            return Response({"value": 3})  # 此用户名已被注册
        if password != password_re:
            return Response({"value": 2})  # 两次密码不一致
        try:
            u = User.objects.create(
                username=name,
                password=password,
                phone=phone,
                is_admin=False
            )
            u.save()
        except Exception as e:
            print(e)
            return Response({"value": 1})  # 注册失败，请联系管理员
        return Response({"value": 0})

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
            elif item.is_baned:
                value = 3
            else:
                # 成功登录
                request.session['username'] = username
        return Response({
            'value': value
        })
