from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Music)
admin.site.register(Profile)
admin.site.register(SongGenre)
admin.site.register(Notifications)
admin.site.register(Package)
admin.site.register(UserPackage)