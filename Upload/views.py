from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
from django.conf import settings
import os
import json
import requests
import random

# Import your ML model's function
from .ocr import process_image  # Replace with your actual function import

class ImageUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            # Save the image
            image_instance = serializer.save()
            image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))
            
            # Process the image with your ML model
            model_result = process_image(image_path)  # Replace with your actual processing function
            model_result = json.loads(model_result)
            print(model_result,type(model_result))

            get_url = 'http://172.20.10.2:10000/api/get-document/' + model_result['id']
            print(get_url)
            
            try:
                response = requests.get(get_url)  # Send the GET request
                if response.status_code == 200:
                    response_data = response.json()  # Parse the response as JSON
                    response_data = json.loads(response_data)                    
                    print(response_data)  # Debugging: print the received data
                    if (response_data['isActive']) and ((response_data['name'],response_data['gender'],response_data['dob'])==(model_result['name'],model_result['gender'].upper(),model_result['DOB'])):
                        return Response({'msg':'validated'}, status=status.HTTP_200_OK)
                    else:
                        print(response_data['name'],response_data['gender'],response_data['dob'],'======',model_result['name'],model_result['gender'],model_result['DOB'])
                        return Response({'msg':'not validated'}, status=status.HTTP_200_OK)                        
                else:
                    return Response({'error': 'Failed to retrieve data from the external API'}, status=status.HTTP_400_BAD_REQUEST)
            except requests.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueDocAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract name, dob, and gender from request
        name = request.data.get('name')
        dob = request.data.get('dob')
        gender = request.data.get('gender')

        # Function to generate random 12-digit ID
        def generate_id():
            return ''.join([str(random.randint(0, 9)) for _ in range(12)])

        # Check if the generated ID is already used
        def is_id_used(id):
            url = f'http://172.20.10.2:10000/api/get-document/{id}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                data = json.loads(data)
                print(data,type(data))
                # If we get valid data, assume the ID is used
                return data.get('id') == id
            return False

        # Loop to generate a new ID until it's unused
        new_id = generate_id()
        while is_id_used(new_id):
            new_id = generate_id()

        # Data to be sent in the POST request
        data = {
            "name": name,
            "dob": dob,
            "gender": gender,
            "id": str(new_id)
        }

        # Send POST request to the external API
        post_url = 'http://172.20.10.2:10000/api/issue-document'
        try:
            post_response = requests.post(post_url, json=data)
            if post_response.status_code == 200:
                # response_data = post_response.json()
                # Return the external API's response
                return Response(json.dumps(data), status=status.HTTP_200_OK)
            else:
                # Handle unsuccessful response
                return Response({'error': 'Failed to issue document'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            # Handle exceptions
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)