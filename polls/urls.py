from django.urls import path
from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),  # polls/views 에서 index 뷰에 연결, /polls/
    path('<int:question_id>/', views.detail, name='detail'),  # /polls/1/
    path('<int:question_id>/results/', views.results, name='results'),  # /polls/1/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),  # /polls/1/vote/
    path('add/', views.add, name='add')
]
