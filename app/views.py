from django.shortcuts import render
from app.serializers import *
from app.models import *
from django.http import QueryDict

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime

# Create your views here.


# register **
class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], phone_number=request.POST['phone_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.is_gmail_authenticated = True
        user.save()

        fields = ('id', 'username', 'email', 'phone_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)



# login **
class UserLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)




# add-ebook **
class addEbook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.id
        title = request.data["title"]
        author = request.data["author"]
        genre = request.data["genre"]
        review = request.data["review"]
        is_favorite = request.data["is_favorite"]
        ordinary_dict = {'user': user, 'title': title, 'author': author,
                         'genre': genre, 'review': review, 'is_favorite':is_favorite}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        ebook_details = EbookSerializer(data=query_dict)
        if ebook_details.is_valid():
            ebook_details.save()
            data = {'status': 200, "message": "Ebook added successfully",
                    "data": ebook_details.data}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'status': 400, "message": "can't add Ebook", "error": ebook_details.errors}
            return Response(data, status=status.HTTP_200_OK)


# edit-ebook **
class editEbook(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        ebook = Ebook.objects.get(id=id)
        ebook.title = request.data["title"]
        ebook.author = request.data["author"]
        ebook.genre = request.data["genre"]
        ebook.review = request.data["review"]
        ebook.is_favorite = request.data["is_favorite"]
        ebook.save()
        data = {'status': 200, "message": "ebook updated successfully"}
        return Response(data, status=status.HTTP_200_OK)



# delete-ebook **
class deleteEbook(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        alreadyexist = Ebook.objects.filter(id=id).exists()
        if alreadyexist is True:
            ebboks = Ebook.objects.get(id=id)

            ebboks.is_deleted = True
            ebboks.deleted_at = datetime.datetime.now()
            ebboks.save()
            data = {'status': 400, "message": "ebook deleted successfully"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'status': 400, "message": "ebook doesn't exist"}
            return Response(data, status=status.HTTP_200_OK)



# get_all_ebooks **
class getAllEbooks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        items = Ebook.objects.filter(user=user)
        serializer = EbookSerializer(items, many=True)
        return Response({'data':serializer.data,'status': 200, "message": "success"})
