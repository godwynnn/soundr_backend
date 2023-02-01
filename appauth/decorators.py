from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status


def isAuthenticated(view_func):
    def wrapper_func(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return view_func(self,*args,**kwargs)
        else:
            return Response({
                'message':'authenticated user only'
            })
    return wrapper_func



def isloggedin(view_func):
    def wrapper_func(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return Response({
                'message':'user is logged in'
            })
            
        else:
            return view_func(self,*args,**kwargs)
            
    return wrapper_func
