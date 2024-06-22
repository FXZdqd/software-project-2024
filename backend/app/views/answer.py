from django.db import IntegrityError, transaction
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from app.models import *


class CreateAnswer(APIView):
    def post(self, request):
        # 获取请求中的数据
        username = request.data.get('username')
        question_id = request.data.get('q_id')
        content = request.data.get('content')

        if not all([username, question_id, content]):
            return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            question = Question.objects.get(id=question_id)

            answer = Answer.objects.create(
                user=user,
                question=question,
                content=content
            )
            return Response({
                "message": "Answer created successfully.",
                "answer_id": answer.id
            }, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeAnswer(APIView):
    def post(self, req: Request):
        username = req.data['username']
        a_id = req.data['a_id']  # Answer ID from the request
        try:
            user = User.objects.get(username=username)
            if not a_id:
                return Response({"error": "Missing 'a_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

            answer = Answer.objects.get(id=a_id)
            like, created = UserLikeAnswer.objects.get_or_create(user=user, answer=answer)
            if created:
                answer.likes += 1
                answer.save()
                return Response({"message": "Answer liked successfully."})
            else:
                return Response({"message": "You already liked this answer."}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Could not process like."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DelAnswer(APIView):
    def post(self, req: Request):
        a_id = req.data['a_id']  # Answer ID from the request
        try:
            answer = Answer.objects.get(id=a_id)
            if answer is None:
                return Response({"error": "Answer Not Found"}, status=status.HTTP_404_NOT_FOUND)
            answer.delete()
            return Response({"message": "Answer deleted successfully."}, status=status.HTTP_200_OK)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Could not process delete."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnlikeAnswer(APIView):
    def post(self, req: Request):
        username = req.data['username']
        a_id = req.data['a_id']  # Answer ID from the request
        try:
            user = User.objects.get(username=username)
            if not a_id:
                return Response({"error": "Missing 'a_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

            like = UserLikeAnswer.objects.get(user=user, answer_id=a_id)
            like.answer.likes -= 1
            like.answer.save()
            like.delete()
            return Response({"message": "Answer unliked successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserLikeAnswer.DoesNotExist:
            return Response({"error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Could not process unlike."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckUserLikeAnswer(APIView):
    def get(self, req: Request):
        username = req.query_params.get('username')
        a_id = req.query_params.get('a_id')
        try:
            user = User.objects.get(username=username)
            if not a_id:
                return Response({"error": "Missing 'a_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

            UserLikeAnswer.objects.get(user=user, answer_id=a_id)
            return Response({"liked": True})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserLikeAnswer.DoesNotExist:
            return Response({"liked": False})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportAnswer(APIView):
    def post(self, req: Request):
        a_id = req.data.get('a_id')

        if not a_id:
            return Response({"error": "Missing 'a_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            answer = Answer.objects.get(id=a_id)
            answer.reports += 1
            answer.save()

            # 同时增加提出问题者和提出回答者的举报数
            question = answer.question
            question.user.reports += 1
            question.user.save()
            answer.user.reports += 1
            answer.user.save()

            return Response({"message": "Answer reported successfully."})
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Could not process report."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)