from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status
from app.models import Question, Tag
from django.db.models import Q, Case, When, Value, IntegerField
from django.db.models import Case, When, Value, IntegerField

class GetQuestionsByTag(APIView):
    def post(self, req):
        tag_name = req.data.get('tag_name')
        sort_questions_by = req.data.get('sort_questions_by', 'relevance')
        sort_questions_order = req.data.get('sort_questions_order', 'desc')
        sort_answers_by = req.data.get('sort_answers_by', 'likes')
        sort_answers_order = req.data.get('sort_answers_order', 'desc')

        if not tag_name:
            return Response({"error": "No tag name provided"}, status=400)

        question_sort_options = {
            'likes': 'likes',
            'date': 'date',
            'views': 'views',
            'relevance': 'relevance'
        }
        answer_sort_options = {
            'likes': 'likes',
            'date': 'date'
        }

        question_sort_prefix = '' if sort_questions_order == 'asc' else '-'
        answer_sort_prefix = '' if sort_answers_order == 'asc' else '-'

        try:
            tag = Tag.objects.get(name=tag_name)
            questions = tag.question_set.all()

            if sort_questions_by == 'relevance':
                questions = questions.annotate(
                    relevance=Case(
                        When(title__icontains=tag_name, then=Value(2)),
                        When(content__icontains=tag_name, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ).order_by(question_sort_prefix + 'relevance')
            else:
                questions = questions.order_by(question_sort_prefix + question_sort_options.get(sort_questions_by, 'date'))

            return_data = []
            for question in questions:
                tags = question.tags.all()
                tag_names = [tag.name for tag in tags]
                answers = question.answers.all().order_by(answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))
                answer_data = [{
                    'a_id': answer.id,
                    'content': answer.content,
                    'username': answer.user.username,
                    'date': answer.date,
                    'likes': answer.likes,
                } for answer in answers]
                return_data.append({
                    'q_id': question.id,
                    'title': question.title,
                    'content': question.content,
                    'username': question.user.username,
                    'date': question.date,
                    'tags': tag_names,
                    'answers': answer_data
                })
            return Response({"questions": return_data})
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=404)
        except Exception as e:
            return Response({"error": "An error occurred"}, status=500)


class GetQuestionByKeyword(APIView):
    def post(self, request):
        keyword = request.data.get('keyword')
        sort_questions_by = request.data.get('sort_questions_by', 'relevance')
        sort_questions_order = request.data.get('sort_questions_order', 'desc')
        sort_answers_by = request.data.get('sort_answers_by', 'likes')
        sort_answers_order = request.data.get('sort_answers_order', 'desc')

        if not keyword:
            return Response({"error": "Missing 'keyword' parameter."}, status=400)

        question_sort_options = {
            'likes': 'likes',
            'date': 'date',
            'views': 'views',
            'relevance': 'relevance'
        }
        answer_sort_options = {
            'likes': 'likes',
            'date': 'date'
        }

        question_sort_prefix = '' if sort_questions_order == 'asc' else '-'
        answer_sort_prefix = '' if sort_answers_order == 'asc' else '-'

        questions = Question.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        )

        if sort_questions_by == 'relevance':
            questions = questions.annotate(
                relevance=Case(
                    When(title__icontains=keyword, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by(question_sort_prefix + 'relevance')
        else:
            questions = questions.order_by(question_sort_prefix + question_sort_options.get(sort_questions_by, 'date'))

        data = [{
            'q_id': question.id,
            'title': question.title,
            'content': question.content,
            'date': question.date,
            'likes': question.likes,
            'views': question.views,
            'tags': [tag.name for tag in question.tags.all()],
            'username': question.user.username,
            'answers': [{
                'a_id': answer.id,
                'content': answer.content,
                'date': answer.date,
                'likes': answer.likes,
                'username': answer.user.username
            } for answer in question.answers.all().order_by(answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))]
        } for question in questions]

        return Response(data)


