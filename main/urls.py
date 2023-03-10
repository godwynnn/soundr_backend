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
    path('update/<str:pk>',UpdateMusicView.as_view(),name='update_music'),
    path('add/favourite',AddRemoveFavourite.as_view(),name='add_favourite'),
    # path('remove/favourite',RemoveFromFavourite.as_view(),name='remove_favourite'),
    path('follow',FollowersView.as_view(),name='follow'),
    path('user/profile',UserProfileView.as_view(),name='user_profile'),


    path('packages',Packages.as_view(),name='packages'),
    path('payment',PaymentView.as_view(),name='payment'),

    path('favourite',UserFavourite.as_view(),name='favourite'),
    
]