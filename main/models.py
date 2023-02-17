from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import tree
from .formatchecker import ContentTypeRestrictedFileField
from django.utils.text import slugify
from tinytag import TinyTag
import os
# Create your models here.



class Profile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE,unique=True)
    email=models.EmailField(null=True,blank=True)
    first_name=models.CharField(max_length=100,blank=True, null=True)
    second_name=models.CharField(max_length=100,blank=True, null=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True,blank=True,upload_to='image/users_img',default='image/4762573.jpg')
    followers=models.ManyToManyField(User,blank=True,related_name='followers')
    following=models.ManyToManyField(User,blank=True,related_name='following')
    activation_token=models.CharField(max_length=200,null=True, blank=True)
    date_joined=models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user}'

    class Meta:
        ordering= ['-date_joined']


class SongGenre(models.Model):
    name=models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name


class Package(models.Model):
   
    name=models.CharField(max_length=100,null=True,blank=True)
    limit=models.PositiveIntegerField(null=True,blank=True)
    amount=models.PositiveIntegerField(null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return "{} package".format(self.name)


class UserPackage(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='user_package')
    package=models.ForeignKey(Package,null=True,blank=True,on_delete=models.CASCADE)
    txref=models.CharField(max_length=500,null=True,blank=True)
    ps_txref= models.CharField(max_length=500,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_created']

    def __str__(self):

        return "{} of {}".format(self.package.name,self.user.email)




class Music(models.Model):
    # Genre=(
    #     ('Afro','Afro'),
    #     ('Afro-pop','Afro-pop'),
    #     ('Pop','Pop'),
    #     ('Hip-pop','Hip-pop'),
    # )
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    package=models.ForeignKey(UserPackage,null=True,blank=True,on_delete=models.CASCADE)
    artist_name=models.CharField(max_length=100,blank=True, null=True)
    title=models.CharField(max_length=100,blank=True, null=True)
    price=models.IntegerField(null=True,blank=True,default=0)
    image=models.ImageField(upload_to='image/',default='image/4762573.jpg',null=True,blank=True,)
    slug=models.SlugField(null=True,blank=True)
    # genre=models.CharField(max_length=100,blank=True,null=True, choices=Genre)
    genre=models.ForeignKey(SongGenre,null=True,blank=True,on_delete=models.CASCADE)
    view_count=models.PositiveBigIntegerField(null=True,blank=True,default=0)
    # duration=models.CharField(max_length=20,blank=True,null=True)
    favourite=models.ManyToManyField(User,blank=True,related_name='favourites')
    share_to=models.ManyToManyField(User,blank=True,related_name='share_to')

    audio=models.FileField(upload_to='audio/',blank=True,null=True,)
    description=models.TextField(max_length=1000,null=True,blank=True)
    timestamp=models.DateTimeField(null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def save(self,*args,**kwargs):
        # audio_dirs=os.getcwd()+'/static/'+self.audio.url
        
        # tag = TinyTag.get(audio_dirs)
        # self.duration=str(tag.duration/60)[:4]
        if self.slug==None:
            count=1
            slug=slugify(self.artist_name+'-'+ self.title)

            has_slug=Music.objects.filter(slug=slug)
            while has_slug:
                count+=1
                slug=slugify(self.artist_name+'-'+ self.title)+'-'+str(count)
                has_slug=Music.objects.filter(slug=slug).exists()
            
            self.slug=slug
        
        super().save(*args,**kwargs)
    
    @property
    def song_duration(self):
        audio_dirs=os.getcwd()+'/static/'+self.audio.url
        
        tag = TinyTag.get(audio_dirs)
        duration=tag.duration/60
        return f"{str(duration)[:4]}"

    def __str__(self):
        return f'{self.artist_name}-{self.title}'

    class Meta:
        ordering= ['-date_added']


class Notifications(models.Model):
    from_user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='from_user_notif')
    to_user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='to_user_notif')
    date_followed=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    seen=models.BooleanField(blank=True,default=False)

    def __str__(self):
        return f'From {self.from_user.username} to {self.to_user.username} Notification'

