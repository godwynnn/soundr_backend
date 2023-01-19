from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from knox.auth import AuthToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name','password','email','id','is_staff','is_superuser','is_active')

        extra_kwargs={'password':{'write_only':True},'is_staff':{'read_only':True},'is_superuser':{'read_only':True},'is_active':{'read_only':True}}

    def create(self,validated_data):
        print(validated_data)
        # username=str(validated_data['email']).split('@')[0]
        user = User.objects.create(email=str(validated_data['email']).lower().strip(),
        username=str(validated_data['email']).lower(),
        first_name=str(validated_data['first_name']).lower().strip(),
        last_name=str(validated_data['last_name']).lower().strip(),
        is_active=False
        

        )
        user.set_password(validated_data['password'])
        
        user.save()


        try:
            profile=Profile.objects.get(user=user)
        
        except ObjectDoesNotExist:
            profile=Profile.objects.create(user=user)

        
        try:
            token= AuthToken.objects.get(user=user)
        except ObjectDoesNotExist:
            token=AuthToken.objects.create(user=user)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'