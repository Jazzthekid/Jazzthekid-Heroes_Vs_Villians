from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Super
from .serializers import SuperSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view (['GET','POST'])
def supers_list(request):

    if request.method == 'GET':

        super_type = request.query_params.get('type')
        print(super_type)
        queryset=Super.objects.all()

        if super_type:
            queryset =queryset.filter(super_type__type=super_type)
            serializer = SuperSerializer(queryset, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
       
        else:
            heroes = queryset.filter(super_type__type='Hero')
            villains = queryset.filter(super_type__type="Villain")
            heroes_serializer = SuperSerializer(heroes, many=True)
            villains_serializer = SuperSerializer(villains, many=True)
            custom_response_dict = {
                "Heroes":heroes_serializer.data,
                "Villains": villains_serializer.data,
        }
            return Response(custom_response_dict,status=status.HTTP_200_OK) 
      
       
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status= status.HTTP_201_CREATED)


@api_view (['GET','PUT','DELETE'])
def super_detail(request,pk):
    supers = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(supers)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(supers, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        supers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

                     