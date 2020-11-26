from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('polls_list/', views.get_polls_list),
    path('create_poll/', views.create_poll),
    path('update_poll/<int:poll_id>/', views.update_poll),
    path('delete_poll/<int:poll_id>/', views.delete_poll),
    path('create_question/', views.create_question),
    path('update_question/<int:question_id>/', views.update_question),
    path('delete_question/<int:question_id>/', views.delete_question),
    path('create_choice/', views.create_choice),
    path('update_choice/<int:choice_id>/', views.update_choice),
    path('delete_choice/<int:choice_id>/', views.delete_choice),
    path('active_polls/', views.get_active_polls),
    path('answers/<int:user_id>/', views.get_user_answers),
    path('create_answer/', views.create_answer),
]
