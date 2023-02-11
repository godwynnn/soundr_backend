from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView,RetrieveAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
import mimetypes
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage
from knox.auth import TokenAuthentication
import json
from rest_framework.parsers import FileUploadParser,FormParser,MultiPartParser

from appauth.serializers import *
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from push_notifications.models import APNSDevice, GCMDevice

def UserProfile(user):
    try:
        user_profile=Profile.objects.get(user=user)
        # return user_profile
    except ObjectDoesNotExist:
        user_profile=[]

    return user_profile


def HasMorePost(request):
    if int(request.GET.get('offset')) > Music.objects.all().count():
        return True
    return False


def CreateFollowNotification(request,user_id):
    
    try:
        created_notif=Notifications.objects.filter(from_user=request.user)
        # if user_id != created_notif.to_user.id:
        notification=Notifications.objects.create(
        from_user=request.user,
        to_user=User.objects.get(id=user_id)
        )

        follow=True
    
        
        
    except:
        notification=[]
        follow=False

    return follow
        
# def RecentlyViewed(request,id=None):
#     music_ids=[]
#     if id in music_ids:
#         music_ids.remove(id)
#     else:
#         music_ids.insert(0,id)
    
#     if len(music_ids) > 10:
#         music_ids.pop()
    
#     recently_viewed=Music.objects.filter(id__in=music_ids)
#     # recently_viewed_music=recently_viewed.sort(lambda x: x.id, reverse=True)

#     return recently_viewed



class MusicPaginationLimit(LimitOffsetPagination):
    default_limit = 2
    max_limit = 1000000
    min_limit = 1
    min_offset = 0
    max_offset = 1000000


class LandingPageView(APIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,]
    authentication_classes=[TokenAuthentication]
    pagination_class =MusicPaginationLimit
    

    # limit_query_param  ='limit'

    def get(self,request):
        # print(request.user.id)
        # user=User.objects.get(id=request.user.id) 
        # profile=[]
        musics=self.queryset[:10]
        most_listened=list(Music.objects.all())
        most_listened.sort(key=lambda x:-x.view_count)
        serialized_data=MusicSerializer(musics,many=True).data

        if request.user.is_authenticated:
            musics=Music.objects.all()
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(musics, request)
            serialized_data=MusicSerializer(result_page,many=True).data
            profile=UserProfile(request.user)
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
                data['user_favourite']=False
                if request.user.id in data['favourite']:
                    data['user_favourite']=True

                data['user']=UserSerializer(User.objects.get(id=data['user']), many=False).data

            # recently_viewed=list(Music.objects.filter()).sort(key=lambda x: x.timestamp<timezone.now())  
            recently_viewed=list(Music.objects.filter(timestamp__lt=timezone.now()).order_by('-timestamp'))
            profile_serializer=ProfileSerializer(profile,many=False).data

            # for serializer in profile_serializer:
            profile_serializer['user']=UserSerializer(User.objects.get(id=profile_serializer['user']),many=False).data
            # music=paginator.get_paginated_response(serialized_data)
            # return music
            return Response({
                'profile':profile_serializer,
                'music':serialized_data,
                'music_len':musics.count(),
                'most_listened':MusicSerializer(most_listened,many=True).data,
                'recently_viewed':MusicSerializer(recently_viewed,many=True).data,
                'more_posts':HasMorePost(request)

            })
 
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
            data['user_favourite']=False
            if request.user.id in data['favourite']:
                data['user_favourite']=True

            data['user']=UserSerializer(User.objects.get(id=data['user']), many=False).data

            # recently_viewed=list(Music.objects.filter()).sort(key=lambda x: x.timestamp<timezone.now())  
            recently_viewed=list(Music.objects.filter(timestamp__lt=timezone.now()).order_by('-timestamp'))
        return Response({
            'music':serialized_data,
            'most_listened':MusicSerializer(most_listened,many=True).data,
            'recently_viewed':MusicSerializer(recently_viewed,many=True).data

            
        })


class MusicPlayView(APIView):
    # queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes=[AllowAny,]
    

    def get(self, request,pk):
        music=Music.objects.get(id=pk)
        music.view_count+=1
        music.timestamp=datetime.datetime.now()
        music.save()

        # recently_viewed=RecentlyViewed(request,pk)
        # print(recently_viewed)
        return Response({
            'message':'viewed',
            'music':MusicSerializer(music,many=False).data
        })

class MusicDetailView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly,]
    authentication_classes=[TokenAuthentication,]
    def get(self,request,slug):
        # print(request.Meta)
        music=Music.objects.get(slug=slug)
        if request.user.is_authenticated:
            # music=Music.objects.get(slug=slug)
            profile=UserProfile(request.user)
            profile_serializer=ProfileSerializer(profile,many=False).data
            
            user=[]
            for user_profile in profile_serializer['followers']:
                user_profile=UserSerializer(User.objects.get(id=user_profile),many=False).data
                user.append(user_profile)
            
            profile_serializer['followers']=user
            
            

            return Response({
            'music':MusicSerializer(music,many=False).data,
            'profile':profile_serializer
            })
            
        

        return Response({'music':MusicSerializer(music,many=False).data})

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
                        Q(genre__name__icontains=query)

                         )
        
        return Response({
            'music':MusicSerializer(musics,many=True).data
        })


class MusicView(APIView):
    permission_classes=[AllowAny,]
    def get(self,request):
        all_musics=Music.objects.all().order_by('-date_added')
        print(request.GET.get('page'))

        page=request.GET.get('page')
        paginator=Paginator(all_musics,2)

        try:
            musics=paginator.page(page)
        except PageNotAnInteger:
            musics=paginator.page(1)
        
        except EmptyPage:
            musics=paginator.page(paginator.num_pages)
        
        # print(paginator.num_pages)
        
        return Response({
            'musics':MusicSerializer(musics,many=True).data,
            'num_pages':paginator.num_pages,
            'post_count':paginator.count
        })


class CreateMusicView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]

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
            serialized_data=serializer.save(user=request.user)
            return Response({
                'message':'upload successful',
                'payload':MusicSerializer(serialized_data,many=False).data
            })
        else:
            return Response({
                'message':'invalid data',
                'payload':request.data
            })



class AddToFavourite(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        music_id=request.GET.get('music_id')
        music=Music.objects.get(id=music_id)


        favourite=False
        if request.user in music.favourite.all():
            favourite=True
            return Response({
                'message':'music already added to favorites',
                'favourite':True
            })
        else:
            favourite=True
            music.favourite.add(request.user)
            return Response({
                'message':'added to favourite',
                'favourite':True
            })

        

class RemoveFromFavourite(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        music_id=request.GET.get('music_id')
        music=Music.objects.get(id=music_id)


        favourite=True
        if request.user in music.favourite.all():
            favourite=False
            music.favourite.remove(request.user)
            return Response({
                'message':'music removed favorites',
                'favourite':False
            })
        else:
            favourite=False
            music.favourite.add(request.user)
            return Response({
                'message':'not added to favourite',
                'favourite':False
            })


class FollowersView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user_id=request.GET.get('user_id')

        try:
            profile=Profile.objects.get(user__id=user_id)
        except ObjectDoesNotExist:
            return Response('user don\'t have profile status')

        profile.followers.add(request.user)

        try:
            logged_profile=Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response('user don\'t have profile status')
        
        logged_profile.following.add(profile.user)
        follow=CreateFollowNotification(request,user_id)
        if request.user in profile.followers.all():

            return Response({
                'message': f'following {profile.user}',
                'following':follow,
               
            })

        if profile.user in request.user.following:
            return Response({
                'message': f'following...',
                'following':follow,
               
            })
        
        

class UserProfileView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        profile=UserProfile(request.user)
        profile_serializer=ProfileSerializer(profile,many=False).data

        # for serializer in profile_serializer:
        profile_serializer['user']=UserSerializer(User.objects.get(id=profile_serializer['user']),many=False).data

        return Response({
            'profile':profile_serializer,
        })


class SharePostToFollowersView(APIView):
    def post(self,request):
        user_ids=list(request.data.get('user_ids'))
        pass