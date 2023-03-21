from django.urls import path
from .views import FileUploadView
from . import views

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('upload/', views.upload_file, name='upload_file'),
]
