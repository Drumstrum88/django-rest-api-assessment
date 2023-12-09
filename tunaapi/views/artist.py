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
    
  def list(self, request):
    artist = Artist.objects.all()
    serializer = ArtistSerializer(artist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    artist.name = request.data["name"]
    artist.age = request.data["age"]
    artist.bio = request.data["bio"]
    artist.save()
    
    return Response(None, status=status.HTTP_200_OK)
  
  @action(detail=True, methods=['get'])
  def related(self, request, pk):
        artist = Artist.objects.filter(pk=pk).first()

        if artist:
            artist_genre = artist.genre
            related_artists = Artist.objects.filter(genre=artist_genre).exclude(pk=pk)

            serializer = ArtistSerializer(related_artists, many=True)
            return Response({'artists': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)

  def list(self, request):
    genre_id = request.GET.get('genre')
    if genre_id:
        artists = Artist.objects.filter(genre__id=genre_id)
    else:
        artists = Artist.objects.all()
    
    serializer = ArtistSerializer(artists, many=True)
    return Response({'artists': serializer.data}, status=status.HTTP_200_OK)

class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'name', 'age', 'bio', 'genre']
    
