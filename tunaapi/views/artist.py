from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.artist import Artist
from rest_framework.decorators import action

class ArtistView(ViewSet):
  def create(self, request):
    artist = Artist.objects.create(
      name=request.data["name"],
      age=request.data["age"],
      bio=request.data["bio"],
    )
    
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
  def retrieve(self, request, pk):
    try:
      artist = Artist.objects.get(pk=pk)
      serializer = ArtistSerializer(artist)
      return Response(serializer.data)
    except Artist.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'name', 'age', 'bio']
    
