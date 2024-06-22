from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *
import rest_framework.status
class AddFollowQuestion(APIView):
    def post(self, request):
        username = request.data.get('username')
        question_id = request.data.get('q_id')

        user = User.objects.filter(username=username).first()
        question = Question.objects.filter(id=question_id).first()
        if not user or not question:
            return Response({'message': 'Invalid user or question'}, status=400)

        if UserFollowedQuestion.objects.filter(user=user, question=question).exists():
            return Response({'message': 'Already followed'}, status=400)

        UserFollowedQuestion.objects.create(user=user, question=question)
        return Response({'message': 'Question followed successfully'})


class GetUserFollowedQuestions(APIView):
    def post(self, request):
        username = request.data.get('username')
        print(username)
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({'message': 'User not found'}, status=400)

        followed_questions = UserFollowedQuestion.objects.filter(user=user)
        data = [{
            'q_id': fq.question.id,
            'title': fq.question.title,
            'content': fq.question.content,
            'date': fq.question.date
        } for fq in followed_questions]

        return Response(data)

class UnfollowQuestion(APIView):
    def post(self, request):
        username = request.data.get('username')
        question_id = request.data.get('q_id')

        user = User.objects.filter(username=username).first()
        question = Question.objects.filter(id=question_id).first()
        if not user or not question:
            return Response({'message': 'Invalid user or question'}, status=400)

        followed_question = UserFollowedQuestion.objects.filter(user=user, question=question).first()
        if not followed_question:
            return Response({'message': 'User is not following this question'}, status=400)

        followed_question.delete()
        return Response({'message': 'Successfully unfollowed the question'})