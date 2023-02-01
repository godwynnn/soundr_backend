from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist


# class UserSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['id','email','username','first_name','last_name','password','is_staff','is_superuser']
#         extra_kwargs={'password':{'write_only':True},'is_staff':{'read_only':True},'is_superuser':{'read_only':True}}


#         def create(self,validated_data):
#             user=User.objects.create(
#                 email=validated_data['email'],first_name=validated_data['first_name'],
#                 last_name=validated_data['last_name'],username=validated_data['username']
#             )
#             user.set_password(validated_data['password'])
#             user.save()

#             try:
#                 customer = Profile.objects.get(user=user)
#             except ObjectDoesNotExist:
#                 customer = Profile.objects.create(user=user)


#             return user
        
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Music
        fields='__all__'



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=SongGenre
        fields='__all__'