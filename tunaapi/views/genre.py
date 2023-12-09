from django.db.models import Count
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

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
  
  def retrieve(self, request, pk):
    try:
      genre = Genre.objects.get(pk=pk)
      serializer = GenreSerializer(genre)
      return Response(serializer.data)
    except Genre.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    genre = Genre.objects.all()
    serializer = GenreSerializer(genre, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    genre.save()
    
    return Response(None, status=status.HTTP_200_OK)
  
  @action(detail=False, methods=['get'], url_path='popular')
  def popular(self, request):
        popular_genres = Genre.objects.annotate(song_count=Count('song'))
        serializer = GenreSerializer(popular_genres, many=True)
        return Response({'genres': serializer.data}, status=status.HTTP_200_OK)

  
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ['id', 'description']
