from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

from .models import Question, Poll, Choice, Answer
from .serializers import PollListSerializer, QuestionListSerializer, ChoiceListSerializer, AnswerListSerializer


@csrf_exempt
@api_view(['GET'])
def login(request):
    """Login user with credentials and return token."""
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Username or password is empty'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Incorrect login and password'}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_polls_list(request):
    """Returns all polls."""
    polls = Poll.objects.all()
    serializer = PollListSerializer(polls, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def create_poll(request):
    """Creates poll."""
    serializer = PollListSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        poll = serializer.save()
        return Response(PollListSerializer(poll).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, IsAdminUser))
def update_poll(request, poll_id):
    """Updates poll by its id."""
    poll = get_object_or_404(Poll, pk=poll_id)
    serializer = PollListSerializer(poll, data=request.data, partial=True)
    if serializer.is_valid():
        poll = serializer.save()
        return Response(PollListSerializer(poll).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def delete_poll(request, poll_id):
    """Deletes poll by its id."""
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    return Response("Poll deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def create_question(request):
    """Creates question."""
    serializer = QuestionListSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(QuestionListSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, IsAdminUser))
def update_question(request, question_id):
    """Updates questions by its id."""
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionListSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        question = serializer.save()
        return Response(QuestionListSerializer(question).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def delete_question(request, question_id):
    """Deletes questions by its id."""
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def create_choice(request):
    """Creates choice."""
    serializer = ChoiceListSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save()
        return Response(ChoiceListSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, IsAdminUser))
def update_choice(request, choice_id):
    """Deletes choice by its id."""
    choice = get_object_or_404(Choice, pk=choice_id)
    serializer = ChoiceListSerializer(choice, data=request.data, partial=True)
    if serializer.is_valid():
        choice = serializer.save()
        return Response(ChoiceListSerializer(choice).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def delete_choice(request, choice_id):
    """Deletes choice by its id."""
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.delete()
    return Response("Choice deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_active_polls(request):
    """
    Returns active polls. An active poll is one that satisfies the following condition:
    poll_date_start >= current_user_date >= poll_date_end

    """
    polls = Poll.objects.filter(poll_date_end__gte=timezone.now()).filter(poll_date_start__lte=timezone.now())
    serializer = PollListSerializer(polls, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_answer(request):
    """Creates question."""
    serializer = AnswerListSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        answer = serializer.save()
        return Response(AnswerListSerializer(answer).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_answers(request, user_id):
    """Returns user answers by its id."""
    answers = Answer.objects.filter(user_id=user_id)
    serializer = AnswerListSerializer(answers, many=True)
    return Response(serializer.data)
