from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.genre import Genre

class GenreView(ViewSet):
  def create(self, request):
    genre = Genre.objects.create(
      description=request.data["description"],
    )
    
    serializer = GenreSerializer(genre)
    return Response (serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ['id', 'description']
