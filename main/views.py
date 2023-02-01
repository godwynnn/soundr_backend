from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *

from rest_framework.generics import ListAPIView,RetrieveAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
import mimetypes
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage
from knox.auth import TokenAuthentication
import json

def UserProfile(user):
    try:
        user_profile=Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        user_profile=[]

    return user_profile
        

class LandingPageView(APIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[AllowAny,]

    def get(self,request):
        
        
        musics=Music.objects.all()[:10]
        most_listened=list(Music.objects.all())
        most_listened.sort(key=lambda x:-x.view_count)


        serialized_data=MusicSerializer(musics,many=True).data
        

        for data in serialized_data:
            # data['audio']={}
            data['duration']={}
            data['duration']['val']=''
            duration=''
            for music in musics:
                if music.id == data['id']:
                    # print(music.song_duration)
                    duration=music.song_duration.replace('.',':')
                
            data['duration']['val']=duration
        

        return Response({
            'music':serialized_data,
            'most_listened':MusicSerializer(most_listened,many=True).data
        })


class MusicPlayView(APIView):
    # queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[AllowAny,]
    

    def get(self, request,pk):
        music=Music.objects.get(id=pk)
        music.view_count+=1
        music.save()
        return Response({
            'message':'viewed',
            'music':MusicSerializer(music,many=False).data
        })

class MusicDetailView(APIView):
    permission_classes=[AllowAny,]
    # authentication_classes=[TokenAuthentication,]
    def get(self,request,slug):
        # print(request.Meta)
        music=Music.objects.get(slug=slug)
        

        return Response({
            'music':MusicSerializer(music,many=False).data
        })

class MusicDownloadView(APIView):
    permission_classes=[AllowAny,]
    def get(self, request):
        pk=str(request.GET.get('id'))
        music=Music.objects.get(id=pk)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ',BASE_DIR)
        filename=music.audio.url
        print(filename)

        filepath=BASE_DIR+'/static'+filename
        with open(filepath,'rb') as path:
            file=path.read()
            mime_type, _ = mimetypes.guess_type(filepath)
            response = Response(file, content_type=mime_type)
            # Set the HTTP header for sending to browser
            response['Content-Disposition'] = "attachment; filename=%s" % filename

            return response

        # print('BASE_DIR :',BASE_DIR)


class MusicSearchView(APIView):
    permission_classes=[AllowAny,]
    def get(self,request):
        query=request.GET.get('q')

        musics=Music.objects.filter(
                        Q(artist_name__icontains=query)|
                        Q(title__icontains=query)|
                        Q(slug__icontains=query)|
                        Q(genre__icontains=query)

                         )
        
        return Response({
            'music':MusicSerializer(musics,many=True).data
        })


class MusicView(APIView):
    permission_classes=[AllowAny,]
    def get(self,request):
        all_musics=Music.objects.all()

        page=request.GET.get('page')
        paginator=Paginator(all_musics,1)

        try:
            musics=paginator.page(page)
        except PageNotAnInteger:
            musics=paginator.page(1)
        
        except EmptyPage:
            musics=paginator.page(paginator.num_pages)
        
        print(paginator.num_pages)
        
        return Response({
            'musics':MusicSerializer(musics,many=True).data,
            'num_pages':paginator.num_pages,
            'post_count':paginator.count
        })


class CreateMusicView(APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        genre=SongGenre.objects.all()
        return Response({
            'genre':GenreSerializer(genre,many=True).data
        })


    def post(self,request):


        # genre=SongGenre.objects.get(id=request.data.get('genre'))
        print(request.data)

        serializer=MusicSerializer(data=request.data)
        if serializer.is_valid():
            serialized_data=serializer.save()
            return Response({
                'message':'upload successful',
                'payload':MusicSerializer(serialized_data,many=False).data
            })
        else:
            return Response({
                'message':'invalid data',
                'payload':request.data
            })

        
        # try:
        #     music=Music.objects.create(
        #         artist_name=request.data.get('artist_name'),
        #         title=request.data.get('title'),
        #         image=request.data.get('image'),
        #         audio=request.data.get('audio'),
        #         description=request.data.get('description'),
        #         genre=genre
        #     )
        #     return Response({
        #         'message':'upload successful',
        #         'payload':MusicSerializer(music,many=False).data
        #     })
        # except:
        #     return Response({
        #         'message':'invalid data',
        #         'payload':request.data
        #     })