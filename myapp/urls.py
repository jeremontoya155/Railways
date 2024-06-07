from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.upload_file), name='upload_file'),
    path('files/', login_required(views.file_list), name='file_list'),
    path('files/<int:pk>/', login_required(views.file_detail), name='file_detail'),
]
