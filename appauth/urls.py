from django.urls import path,re_path
from .views import *


urlpatterns=[
   path('register',RegistrationView.as_view(),name='register'),
   path('login',LoginView.as_view(),name='login'),
   path('logout',LogoutView.as_view(),name='logout'),
   # path('api/register-by-access-token/social/<str:backend>/', register_by_access_token),
   re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', register_by_access_token),

    
]