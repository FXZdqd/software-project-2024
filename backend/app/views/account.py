from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from app.models import *


class DeleteUser(APIView):
    def post(self, req: Request):
        username = req.data['username']
        password = req.data['password']
        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if password != user.password:
                return Response({"message": f"Password Incorrect"})
            else:
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
            if not user.is_baned:  # Check if the user is already banned
                user.is_baned = True
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

class AdminRegister(APIView):
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
                is_admin=True
            )
            u.save()
        except Exception as e:
            print(e)
            return Response({"value": 1})  # 注册失败，请联系管理员
        return Response({"value": 0})


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
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password_re = data.get('new_password_re')

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"value": 3})  # 用户不存在
        if old_password != user.password:
            print(old_password)
            print(user.password)
            return Response({"value": 4})
        # 检查两次输入的密码是否一致
        if new_password != new_password_re:
            return Response({"value": 2})  # 两次密码不一致

        # 更新密码
        try:
            user.password = new_password
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
            username = req.data.get('username')  # 得到用户名
            user = User.objects.get(username=username)  # 查找用户对象

            try:
                avatar = Avator.objects.get(user=user)
            except Avator.DoesNotExist:
                avatar = Avator.objects.create(
                    user=user,
                )

            filename = f"{user.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.jpg"
            print(filename)
            avatar.file.save(filename, file, save=True)
            avator_id = avatar.id
            value = 0
        except User.DoesNotExist:
            value = 2  # 用户不存在
        except Exception as e:
            print(e)
            value = 1  # 其他异常

        return Response({
            'value': value,
            'avator_id': avator_id,
        })
def changePicPath(path):
    with open(path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded_data = base64.b64encode(image_data)
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message

# class GetAvatar(APIView):
#     def post(self, req: Request):
#         username = req.data['username']
#         path = ''
#         user = User.objects.get(username=username)
#         value = -1
#         if not Avator.objects.filter(user=user).exists():
#             return Response({
#                 'value': value,
#                 'path': None,
#                 'base64': None
#             })
#         try:
#             pic = Avator.objects.get(user=user)
#             path = pic.file.path
#             value = 0
#         except Exception as e:
#             print(e)
#             value = 1
#         return Response({
#             'value': value,
#             'path': path,
#             'base64': changePicPath(path)
#         })
class GetAvatar(APIView):
    def post(self, req: Request):
        username = req.data['username']

        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            avatar = Avator.objects.filter(user=user).first()

            if avatar:
                return Response({
                    'value': 0,
                    'url': avatar.file.url
                })
            else:
                return Response({
                    'value': -1,  # 没有头像
                    'url': None
                })

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class SetUserInfo(APIView):
    def post(self, req: Request):
        username = req.data.get('username')
        gender = req.data.get('gender')
        grade = req.data.get('grade')
        department = req.data.get('department')

        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)

            if gender is not None:
                user.gender = gender
            if grade is not None:
                user.grade = grade
            if department is not None:
                user.department = department

            user.save()

            return Response({"message": "User info updated successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class GetUser(APIView):
    def post(self, req: Request):
        username = req.data.get('username')

        if not username:
            return Response({"error": "Missing 'username' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)

            # 构造用户信息，排除密码字段
            user_info = {
                'username': user.username,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'is_banned': user.is_baned,
                'reports': user.reports,
                'gender': user.gender,
                'grade': user.grade,
                'department': user.department,
            }

            return Response(user_info)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
