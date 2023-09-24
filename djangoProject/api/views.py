import io

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status

from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Userinfo
from .models import imgr
from .serializers import UserSerializer
from .serializers import ImgSerializer

from django.http import JsonResponse
from django.views import View
# Create your views here.
def home_view(request, *args,**kwargs):
    return render(request,"index.html", {})
@method_decorator(csrf_exempt, name='dispatch') #for post method, will prevent Cross-Site Request Forgery
#i.e csrf attack protection
class UserApi(View):
    #want to see the data? the below function is needed
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            userobj = Userinfo.objects.get(id=id)
            serializer = UserSerializer(userobj)
            return JsonResponse(serializer.data, safe=True, content_type='application/json')

        userobj = Userinfo.objects.all()
        serializer = UserSerializer(userobj, many=True)
        return JsonResponse(serializer.data, safe=False, content_type='application/json')

    #creating user info data
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = UserSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data created'}
            return JsonResponse(res, safe=False, content_type='application/json')

    #Update user data (partial enabled)
    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        userobj = Userinfo.objects.get(id=id)
        serializer = UserSerializer(userobj, data=pythondata, partial=True)
        #To disable partial data remove the 'partial' argument in the above function call
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Updated'}
            return JsonResponse(res, safe=False, content_type='application/json')

        return JsonResponse(serializer.errors, safe=False, content_type='application/json')

    #Delete User data
    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        userobj = Userinfo.objects.get(id=id)
        userobj.delete()
        res = {'msg': 'Data Deleted'}
        return JsonResponse(res, safe=False, content_type='application/json')

class imgView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = imgView.objects.all()
        serializer = ImgSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        img_serializer = ImgSerializer(data=request.data)
        if img_serializer.is_valid():
            img_serializer.save()
            # Retrieve the ID of the newly created image
            new_image_id = img_serializer.instance.id
            # Include the ID in the response
            response_data = {
                'id': new_image_id,  # Include the ID here
                'msg': 'Image data Created'
            }

            return Response(img_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', img_serializer.errors)
            return Response(img_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            image_id = kwargs.get('pk')  # Assuming you pass the image ID in the URL
            image = imgr.objects.get(pk=image_id)
        except imgr.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        img_serializer = ImgSerializer(image, data=request.data)
        if img_serializer.is_valid():
            img_serializer.save()
            return Response(img_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(img_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
