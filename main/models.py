from django.db import models

# Create your models here.



class Singer(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name



class MusicDirector(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name



class Actor(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL' )
  

    def __str__(self):
        return self.Name  



class Lyricist(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name

class MovieName(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
    # MovieCast  = models.ManyToManyField(Actor)

  

    def __str__(self):
        return self.Name
 




class Category(models.Model):
    Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name        



class Year(models.Model):
    Year = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Year        

class Song(models.Model):
    SongName = models.CharField(max_length = 250 , default = 'NULL')
    Singer = models.ManyToManyField(Singer, null = True)
    MusicDirector = models.ManyToManyField(MusicDirector, null = True)
    Lyricist = models.ManyToManyField(Lyricist, null = True)
    MovieName = models.ForeignKey(MovieName, on_delete=models.CASCADE, null = True)
    Cast  = models.ManyToManyField(Actor, null = True)
    YoutubeLink = models.CharField(max_length = 250 , default = 'NULL', null = True)
    Category = models.ManyToManyField(Category, null = True)
    # Category  = models.ForeignKey(Category, on_delete=models.CASCADE, null = True)
    # lyrics  = models.CharField(max_length = 250 , default = 'NULL')
    year  = models.ForeignKey(Year, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.SongName

class UserData(models.Model):
    Fbid = models.CharField(max_length = 250)
    State = models.CharField(max_length = 250 , default = 'NULL')

    Singer = models.ManyToManyField(Singer, null = True)

    Lyricist = models.ManyToManyField(Lyricist, null = True)
    MovieName = models.ForeignKey(MovieName, on_delete=models.CASCADE, null = True)
    Category = models.ManyToManyField(Category, null = True)
    # issue = models.CharField(max_length = 1000, default = 'NULL')
    year  = models.ForeignKey(Year, on_delete=models.CASCADE, null = True)







