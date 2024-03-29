from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *


class CreateQuestion(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        title = data['title']
        content = data['content']
        q_id = -1
        value = -1
        try:
            user = User.objects.get(username=username)
            question = Question.objects.create(
                title=title,
                content=content,
                user=user,
            )
            q_id = question.id
            question.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value, 'q_id': q_id})


class GetQuestion(APIView):
    def post(self, req: Request):
        q_id = req.data['q_id']
        question = Question.objects.get(id=q_id)  # 根据主键查找
        return Response({
            'title': question.title,
            'content': question.content,
            'username': question.user.username,
            'date': question.date
        })

    def get(self, req: Request):
        q_id = req.query_params.get('q_id')
        if not q_id:
            return Response({"error": "No q_id provided"}, status=400)

        question = Question.objects.get(id=q_id)  # 根据主键查找
        return Response({
            'title': question.title,
            'content': question.content,
            'username': question.user.username,
            'date': question.date
        })


class DeleteQuestion(APIView):
    def post(self, req: Request):
        q_id = req.data['q_id']
        value = 1
        try:
            Question.objects.get(id=q_id).delete()
            value = 0
        except Exception as e:
            print(e)
        return Response(value)

class ChangeQuestion(APIView):
    def post(self, req: Request):
        data = req.data
        q_id = data['q_id']
        title = data['title']
        content = data['content']
        value = -1
        try:
            question = Question.objects.get(id=q_id)
            if title != '':
                question.title = title
            if content != '':
                question.content = content
            question.save()
            value = 0
        except Exception as e:
            print(e)
            value = -1
        return Response({
            'value': value
        })

class GetAllQuestions(APIView):
    def post(self, req: Request):
        return_data = []
        allQ = Question.objects.all()
        for q in allQ:
            return_data.append({
                'q_id': q.id,
                'title': q.title,
                'content': q.content,
                'username': q.user.username,
                'date': q.date
            })
        return Response({
            "allQuestion": return_data
        })

