from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status
from app.models import Question, Tag, UserLikeQuestion, UserFollowedQuestion, User, UserLikeAnswer, Answer,Avator
from django.db.models import Q, Case, When, Value, IntegerField
from django.db.models import Case, When, Value, IntegerField


class GetQuestionsByTagUser(APIView):
    def post(self, req):
        tag_name = req.data.get('tag_name')
        username = req.data.get('username')
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
        user = User.objects.get(username=username)
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
                questions = questions.order_by(
                    question_sort_prefix + question_sort_options.get(sort_questions_by, 'date'))

            return_data = []
            for question in questions:
                is_liked = UserLikeQuestion.objects.filter(user=user, question=question).exists()
                is_followed = UserFollowedQuestion.objects.filter(user=user, question=question).exists()
                tags = question.tags.all()
                tag_names = [tag.name for tag in tags]
                answers = question.answers.all().order_by(
                    answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))
                answer_data = [{
                    'a_id': answer.id,
                    'content': answer.content,
                    'username': answer.user.username,
                    'date': answer.date,
                    'likes': answer.likes,
                    'is_liked': UserLikeAnswer.objects.filter(user=user, answer=answer).exists()
                } for answer in answers]
                return_data.append({
                    'q_id': question.id,
                    'title': question.title,
                    'content': question.content,
                    'username': question.user.username,
                    'date': question.date,
                    'tags': tag_names,
                    'is_liked': is_liked,
                    'is_followed': is_followed,
                    'answers': answer_data
                })
            return Response({"questions": return_data})
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=404)
        except Exception as e:
            return Response({"error": "An error occurred"}, status=500)


class GetQuestionByKeywordUser(APIView):
    def post(self, request):
        keyword = request.data.get('keyword')
        username = request.data.get('username')
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
        user = User.objects.get(username=username)
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
            'is_liked': UserLikeQuestion.objects.filter(user=user, question=question).exists(),
            'is_followed': UserFollowedQuestion.objects.filter(user=user, question=question).exists(),
            'answers': [{
                'a_id': answer.id,
                'content': answer.content,
                'date': answer.date,
                'likes': answer.likes,
                'username': answer.user.username,
                'is_liked': UserLikeAnswer.objects.filter(user=user, answer=answer).exists(),
            } for answer in
                question.answers.all().order_by(answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))]
        } for question in questions]

        return Response(data)


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
                questions = questions.order_by(
                    question_sort_prefix + question_sort_options.get(sort_questions_by, 'date'))

            return_data = []
            for question in questions:
                tags = question.tags.all()
                tag_names = [tag.name for tag in tags]
                answers = question.answers.all().order_by(
                    answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))
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
            } for answer in
                question.answers.all().order_by(answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))]
        } for question in questions]

        return Response(data)

import base64
def changePicPath(path):
    with open(path, "rb") as image_file:
        # 读取文件
        image_data = image_file.read()
        base64_encoded_data = base64.b64encode(image_data)
        # 将Base64编码的数据转换为字符串
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message
class SearchUser(APIView):
    def post(self, req):
        keyword = req.data.get('keyword')

        if not keyword:
            return Response({"error": "Missing 'keyword' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 使用icontains进行不区分大小写的模糊匹配
            users = User.objects.filter(username__icontains=keyword)

            # 构造用户信息列表
            user_info_list = []
            for user in users:
                user_info = {
                    'username': user.username,
                    'phone': user.phone,
                    'is_admin': user.is_admin,
                    'is_banned': user.is_baned,
                    'reports': user.reports,
                    'gender': user.gender,
                    'grade': user.grade,
                    'department': user.department,
                    # 其他字段依次添加
                }

                # 获取用户头像并转换为base64编码
                try:
                    avatar = Avator.objects.get(user=user)
                    user_info['base64'] = changePicPath(avatar.file.path)
                except Avator.DoesNotExist:
                    user_info['base64'] = None

                user_info_list.append(user_info)

            return Response({"users": user_info_list})
        except User.DoesNotExist:
            return Response({"error": "No users found matching the keyword."}, status=status.HTTP_404_NOT_FOUND)



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
            } for answer in
                question.answers.all().order_by(answer_sort_prefix + answer_sort_options.get(sort_answers_by, 'likes'))]
        } for question in questions]

        return Response(data)


class GetQuestionAskedByUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        questions = user.question_set.all()
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
            } for answer in
                question.answers.all()]
        } for question in questions]

        return Response(data)


class GetQuestionAnsweredByUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        questions = Question.objects.filter(answers__user=user).distinct()
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
            } for answer in
                question.answers.all()]
        } for question in questions]

        return Response(data)

class GetAllUserByReport(APIView):
    def post(self, request):
        # 获取所有用户，并按照报告数量从高到低排序
        all_users = User.objects.all().order_by('-reports')

        # 构造用户信息列表
        user_info_list = []
        for user in all_users:
            user_info = {
                'username': user.username,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'is_banned': user.is_baned,
                'reports': user.reports,
                'gender': user.gender,
                'grade': user.grade,
                'department': user.department,
                # 其他字段依次添加
            }
            user_info_list.append(user_info)

        return Response({"users": user_info_list})


class GetAllQuestionByReport(APIView):
    def post(self, request):
        # 获取所有问题，并按照报告数量从高到低排序
        all_questions = Question.objects.all().order_by('-reports')

        # 构造问题信息列表
        questions_info_list = []
        for question in all_questions:
            # 构造问题信息
            question_info = {
                'q_id': question.id,
                'title': question.title,
                'content': question.content,
                'date': question.date,
                'reports': question.reports,
                'likes': question.likes,
                'views': question.views,
                # 其他字段依次添加
            }

            # 获取问题的所有回答，并按照报告数量从高到低排序
            answers = question.answers.all().order_by('-reports')

            # 构造回答信息列表
            answers_info_list = []
            for answer in answers:
                answer_info = {
                    'content': answer.content,
                    'date': answer.date,
                    'user': answer.user.username,
                    'likes': answer.likes,
                    'reports': answer.reports,
                    # 其他字段依次添加
                }
                answers_info_list.append(answer_info)

            # 将回答信息列表添加到问题信息中
            question_info['answers'] = answers_info_list

            # 将问题信息添加到问题信息列表
            questions_info_list.append(question_info)

        return Response({"questions": questions_info_list})

