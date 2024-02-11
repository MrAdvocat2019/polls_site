from django.urls import path, include
from . import views
app_name="polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.QuestionDetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/nullask/",views.nullask, name="nullask"),
    path('createnew/', views.create_new_question, name="create_new_question"),
    path('createnewchoice/', views.create_question_with_choices, name="create_new_choice_question"),
    path('<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete')
]