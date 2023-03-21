from django.urls import path
from .views import FileUploadView
from . import views

urlpatterns = [
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/upload_file/', views.upload_file, name='upload_file'),
]
