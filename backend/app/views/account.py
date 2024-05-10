from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from app.models import *


class DeleteUser(APIView):
    def delete(self, req: Request):
        username = req.query_params.get('username')
        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response({"message": f"User '{username}' deleted successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BanUser(APIView):
    def post(self, req: Request):
        username = req.data.get('username')
        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if not user.is_banned:  # Check if the user is already banned
                user.is_banned = True
                user.save()
                return Response({"message": f"User '{username}' has been successfully banned."})
            else:
                return Response({"message": f"User '{username}' is already banned."}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        phone = str(data.get('phone'))
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


class UpdateUsername(APIView):
    def post(self, request):
        data = request.data
        ole_username = data.get('old_username')
        new_username = data.get('new_username')

        user = User.objects.filter(username=ole_username).first()
        if not user:
            return Response({"value": 3})  # 用户不存在

        if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
            return Response({"value": 2})  # 新用户名已被注册

        # 更新用户名
        try:
            user.username = new_username
            user.save()
        except Exception as e:
            print(e)
            return Response({"value": 1})  # 更新失败，请联系管理员

        return Response({"value": 0})  # 更新成功


class UpdatePassword(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        new_password = data.get('new_password')
        new_password_re = data.get('new_password_re')

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"value": 3})  # 用户不存在

        # 检查两次输入的密码是否一致
        if new_password != new_password_re:
            return Response({"value": 2})  # 两次密码不一致

        # 更新密码
        try:
            user.set_password(new_password)
            user.save()
        except Exception as e:
            print(e)
            return Response({"value": 1})  # 更新失败，请联系管理员

        return Response({"value": 0})  # 更新成功




class GetAllUsers(APIView):
    def post(self, request):
        return_data = []
        all_users = User.objects.all()
        for user in all_users:
            return_data.append({
                'user_id': user.id,
                'username': user.username,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'is_baned': user.is_baned
            })
        return Response({
            "allUsers": return_data
        })


import base64


def changePicPath(path):
    with open(path, "rb") as image_file:
        # 读取文件
        image_data = image_file.read()
        # 对数据进行Base64编码
        base64_encoded_data = base64.b64encode(image_data)
        # 将Base64编码的数据转换为字符串
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message


class SetAvatar(APIView):
    def post(self, req: Request):
        value = -1
        avator_id = -1
        file = req.FILES.get('photo')
        try:
            username = req.data['username']  # 得到用户名
            user = User.objects.get(username=username)  # 查找用户对象
            try:
                item = Avator.objects.get(user=user)
                item.file = file
                item.save()
                avator_id = item.id
            except Avator.DoesNotExist:
                pic = Avator.objects.create(
                    file=file,
                    user=user,
                )
                pic.save()
                avator_id = pic.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'avator_id': avator_id,
        })


class GetAvatar(APIView):
    def post(self, req: Request):
        username = req.data['username']
        path = ''
        try:
            user = User.objects.get(username=username)
            pic = Avator.objects.get(user=user)
            path = pic.file.path
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'path': path,
            'base64': changePicPath(path)
        })
