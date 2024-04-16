from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *

class AddFollowQuestion(APIView):
    def post(self, request):
        user_id = request.data.get('username')
        question_id = request.data.get('q_id')

        # 获取用户和问题实例
        user = User.objects.filter(username=user_id).first()
        question = Question.objects.filter(id=question_id).first()
        if not user or not question:
            return Response({'message': 'Invalid user or question'}, status=400)

        # 检查是否已经关注过
        if FollowedQuestion.objects.filter(user=user, question=question).exists():
            return Response({'message': 'Already followed'}, status=400)

        # 创建关注关系
        FollowedQuestion.objects.create(user=user, question=question)
        return Response({'message': 'Question followed successfully'})


class GetUserFollowedQuestions(APIView):
    def get(self, request):
        user_id = request.data.get('username')
        user = User.objects.filter(username=user_id).first()
        if not user:
            return Response({'message': 'User not found'}, status=404)

        followed_questions = user.followed_questions.all()
        data = [{
            'q_id': fq.question.id,
            'title': fq.question.title,
            'content': fq.question.content,
            'date_followed': fq.date_followed
        } for fq in followed_questions]

        return Response(data)
