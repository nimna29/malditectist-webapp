from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
from google.cloud import storage
from .ml import classify_file
from rest_framework import status
from rest_framework.decorators import api_view
from firebase import bucket
from datetime import timedelta


class FileUploadView(APIView):
    def post(self, request, format=None):
        file_obj = request.FILES['file']
        if not file_obj.name.endswith('.exe'):
            return Response({'error': 'Invalid file type. Only .exe files are supported.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        unique_key = request.data.get('unique_key')
        if unique_key is None:
            return Response({'error': 'Unique key not found in request.'}, status=status.HTTP_400_BAD_REQUEST)

        filename = default_storage.save(file_obj.name, file_obj)
        uploaded_file_url = os.path.join(settings.MEDIA_URL, filename)

        # Upload the file to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(os.path.join(settings.MEDIA_ROOT, filename))

        # Send response to frontend
        return Response({'uploaded_file_url': uploaded_file_url}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    if file is None:
        return Response({'error': 'File not found in request'}, status=status.HTTP_400_BAD_REQUEST)

    if not file.name.endswith('.exe'):
        return Response({'error': 'Invalid file type. Only .exe files are supported.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    unique_key = request.data.get('unique_key')
    if unique_key is None:
        return Response({'error': 'Unique key not found in request.'}, status=status.HTTP_400_BAD_REQUEST)

    # Upload the file to Firebase Storage
    filename = f"{unique_key}_{file.name}"
    blob = bucket.blob(filename)
    blob.upload_from_file(file)

    # Get the public URL of the uploaded file
    # file_url = blob.public_url

    # Get the private URL of the uploaded file
    file_url = blob.generate_signed_url(
        expiration=timedelta(minutes=30), method='GET')

    # Pass the file to the classify_file function for analysis
    result = classify_file(file)
    if result is None:
        return Response({'error': 'Failed to classify file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(result, status=status.HTTP_200_OK)
