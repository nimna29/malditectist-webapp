from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def home(request):
    return HttpResponse("<h1>Hello World!</h1>")

# class FileUploadView(APIView):
#     def post(self, request, format=None):
#         uploaded_file = request.FILES['file']
#         file_url = upload_to_firebase(uploaded_file)

#         return Response({'url': file_url}, status=status.HTTP_201_CREATED)

