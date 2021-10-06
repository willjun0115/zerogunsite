from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:board_id>/', views.board, name='board'),
    path('<int:board_id>/post/', views.post, name='post'),
    path('<str:post_id>/like/', views.like, name='like'),
    path('setting/', views.setting, name='setting'),
]