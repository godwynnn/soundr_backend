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



class LandingPageView(APIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[AllowAny,]

    def get(self,request):
        
        
        musics=Music.objects.all()[:10]
        
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
            'music':serialized_data
        })


class MusicPlayView(RetrieveAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[AllowAny,]
    

    # def get(self, request,pk):
    #     music=Music.objects.get(id=pk)
    #     view=0
    #     music.view_count=view+1
    #     music.save()
    #     return Response({
    #         'message':'viewed',
    #         'music':MusicSerializer(music,many=False).data
    #     })

class MusicDetailView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[TokenAuthentication,]
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