from django.db import IntegrityError
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from app.models import *


class CreateQuestion(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        title = data['title']
        content = data['content']
        tags = data.get('tags', [])  # 从请求中获取标签列表
        q_id = -1
        value = -1
        try:
            user = User.objects.get(username=username)
            question = Question.objects.create(
                title=title,
                content=content,
                user=user,
            )
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)  # 确保标签存在
                question.tags.add(tag)  # 添加标签到问题
            question.save()
            q_id = question.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value, 'q_id': q_id})


class ChangeQuestion(APIView):
    def post(self, req: Request):
        data = req.data
        q_id = data['q_id']
        title = data['title']
        content = data['content']
        tags = data.get('tags')  # 新的标签列表
        value = -1
        try:
            question = Question.objects.get(id=q_id)
            if title:
                question.title = title
            if content:
                question.content = content
            if tags is not None:
                question.tags.clear()
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)
            question.save()
            value = 0
        except Exception as e:
            print(e)
            value = -1
        return Response({'value': value})


class DeleteQuestion(APIView):
    def post(self, req: Request):
        q_id = req.data['q_id']
        value = 1
        try:
            question = Question.objects.get(id=q_id)
            question.delete()
            value = 0
        except Exception as e:
            print(e)
        return Response({'value': value})


class GetAllQuestions(APIView):
    def post(self, req: Request):
        return_data = []
        all_questions = Question.objects.prefetch_related('answers').all()  # Prefetch answers to reduce database hits
        for question in all_questions:
            tags = question.tags.all()
            tag_names = [tag.name for tag in tags]
            answers = question.answers.all()  # Fetch all answers related to the question
            answer_data = [{
                'a_id': answer.id,
                'content': answer.content,
                'username': answer.user.username,
                'date': answer.date,
                'likes': answer.likes,
            } for answer in answers]  # Serialize answer data
            return_data.append({
                'q_id': question.id,
                'title': question.title,
                'content': question.content,
                'username': question.user.username,
                'date': question.date,
                'tags': tag_names,
                'answers': answer_data  # Include answers in the response
            })
        return Response({
            "allQuestions": return_data
        })



class LikeQuestion(APIView):
    def post(self, req: Request):
        username = req.data['username']
        q_id = req.data['q_id']
        user = User.objects.get(username=username)
        if q_id is None:
            return Response({"error": "Missing 'q_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Question.objects.get(id=q_id)
            like, created = UserLikeQuestion.objects.get_or_create(user=user, question=question)
            if created:
                question.likes += 1
                question.save()
                return Response({"message": "Question liked successfully."})
            else:
                return Response({"message": "You already liked this question."}, status=status.HTTP_409_CONFLICT)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Could not process like."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnlikeQuestion(APIView):
    def post(self, req: Request):
        username = req.data['username']
        q_id = req.data['q_id']
        user = User.objects.get(username=username)

        if not q_id:
            return Response({"error": "Missing 'q_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            like = UserLikeQuestion.objects.get(user=user, question_id=q_id)
            like.question.likes -= 1
            like.question.save()
            like.delete()
            return Response({"message": "Question unliked successfully."})
        except UserLikeQuestion.DoesNotExist:
            return Response({"error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)


class CheckUserLikeQuestion(APIView):
    def get(self, req: Request):
        username = req.query_params.get('username')
        q_id = req.query_params.get('q_id')
        try:
            user = User.objects.get(username=username)
            if not q_id:
                return Response({"error": "Missing 'q_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

            UserLikeQuestion.objects.get(user=user, question_id=q_id)
            return Response({"liked": True})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserLikeQuestion.DoesNotExist:
            return Response({"liked": False})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
