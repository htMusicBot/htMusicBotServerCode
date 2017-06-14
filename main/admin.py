from django.contrib import admin

from main.models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song , UserData



# Register your models here.
admin.site.register(Singer)
admin.site.register(MusicDirector)
admin.site.register(Lyricist)
admin.site.register(MovieName)
admin.site.register(Actor)
admin.site.register(Category)
admin.site.register(Year)
admin.site.register(Song)
admin.site.register(UserData)