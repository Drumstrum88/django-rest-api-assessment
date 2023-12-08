from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from tunaapi.models.song import Song
from tunaapi.models.artist import Artist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'album', 'length', 'artist']

class SongView(ViewSet):
    def create(self, request):
        try:
            artist_id = request.data.get('artist_id')
            title = request.data.get('title')
            album = request.data.get('album')
            length = request.data.get('length')
            
            try:
                artist = Artist.objects.get(pk=artist_id)
            except Artist.DoesNotExist:
                return Response(
                    {'message': 'Artist does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            song = Song.objects.create(
                title=title,
                album=album,
                length=length,
                artist=artist, 
            )
            
            serializer = SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {'message': f'Missing key: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
