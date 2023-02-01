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


class Music(models.Model):
    # Genre=(
    #     ('Afro','Afro'),
    #     ('Afro-pop','Afro-pop'),
    #     ('Pop','Pop'),
    #     ('Hip-pop','Hip-pop'),
    # )
    artist_name=models.CharField(max_length=100,blank=True, null=True)
    title=models.CharField(max_length=100,blank=True, null=True)
    price=models.IntegerField(null=True,blank=True,default=0)
    image=models.ImageField(upload_to='image/',default='image/4762573.jpg',null=True,blank=True,)
    slug=models.SlugField(null=True,blank=True)
    # genre=models.CharField(max_length=100,blank=True,null=True, choices=Genre)
    genre=models.ForeignKey(SongGenre,null=True,blank=True,on_delete=models.CASCADE)
    view_count=models.PositiveBigIntegerField(null=True,blank=True,default=0)
    # duration=models.CharField(max_length=20,blank=True,null=True)
    favourite=models.ManyToManyField(User,blank=True)
    audio=models.FileField(upload_to='audio/',blank=True,null=True,)
    description=models.TextField(max_length=1000,null=True,blank=True)
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
