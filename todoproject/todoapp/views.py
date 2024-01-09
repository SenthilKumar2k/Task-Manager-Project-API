from .models import User,Todolist
from .serializers import UserSerializer, TodolistSerializer, LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegistrationView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'user created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class Loginview(APIView):    
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=User.objects.get(username=serializer.validated_data['username'])
        refresh=RefreshToken.for_user(user)
        return Response({'refresh':str(refresh),'access':str(refresh.access_token)},status=status.HTTP_200_OK)
        
class TaskAssignView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user=request.user
        print(user)
        serializer_data={**request.data,'username':user.id}
        serializer=TodolistSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'task added successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request,id):
        data=User.objects.get(id=id)
        datas=Todolist.objects.filter(username=id)
        serializer=UserSerializer(data)
        serialiser=TodolistSerializer(datas, many=True)
        return Response({'User':serializer.data,'Todolist':serialiser.data}, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            user_data=request.data.get('User',{})
            print(user_data)
            todolist_data=request.data.get('Todolist',[])
            print(todolist_data)
            instance=User.objects.get(id=id)
            instances=Todolist.objects.filter(username=id)
            serializer=UserSerializer(instance, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
            serialisers=[TodolistSerializer(instan, data=todolist, partial=True) for instan,todolist in zip(instances,todolist_data)]
            if all(serialiser.is_valid() for serialiser in serialisers):
                for serialiser in serialisers:
                    serialiser.save()
                return Response({'user':serializer.data,"todolist":[serialiser.data for serialiser in serialisers]},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Todolist data is not valid'}, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            return Response({'Error Message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        try:
            todolist_item=Todolist.objects.get(id=id)
        except Todolist.DoesNotExist:
            return Response({'message':'Todolist item not Found'}, status=status.HTTP_404_NOT_FOUND)
        todolist_item.delete()
        return Response({'message':'The task deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    

class TaskCheckView(APIView):
    def delete(self,request,id):
        user_item=User.objects.get(id=id)
        user_item.delete()
        todolist_item=Todolist.objects.filter(username=id)
        for todolist in todolist_item:
            todolist.delete()
        return Response({'message':'usersuccessfully deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get(self,request,id):
        user_item=User.objects.get(id=id)
        todolist_item=Todolist.objects.filter(username=id)
        todo_serializer=[]
        for todo in todolist_item:
            if todo.completed:
                todo_serializer.append(todo)
        user_serializer=UserSerializer(user_item)
        todo_serialiser=TodolistSerializer(todo_serializer, many=True)
        return Response({'User':user_serializer.data,'User completed tasks':todo_serialiser.data},status=status.HTTP_200_OK)
    
class TaskCheckApiView(APIView):
    def get(self,request,id):
        user_item=User.objects.get(id=id)
        todolist_item=Todolist.objects.filter(username=id)
        todo_serializer=[]
        for todo in todolist_item:
            if not(todo.completed):
                todo_serializer.append(todo)
        user_serializer=UserSerializer(user_item)
        todo_serialiser=TodolistSerializer(todo_serializer,many=True)
        return Response({'User':user_serializer.data,'User incompleted Tasks':todo_serialiser.data},status=status.HTTP_200_OK)
