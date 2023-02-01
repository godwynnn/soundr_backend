from django.urls import path
from .views import *

urlpatterns=[
    path('',LandingPageView.as_view(),name='music'),
    path('<str:slug>/',MusicDetailView.as_view(),name='music_detail'),
    path('<str:pk>/play',MusicPlayView.as_view(),name='music_play'),
    path('download',MusicDownloadView.as_view(),name='music_download'),
    path('search',MusicSearchView.as_view(),name='music_search'),
    path('recent',MusicView.as_view(),name='music_search'),
    path('create',CreateMusicView.as_view(),name='create_music'),
    
]