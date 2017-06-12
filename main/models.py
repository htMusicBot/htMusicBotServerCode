from django.db import models

# Create your models here.



class Singer(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name



class MusicDirector(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name




class Lyricist(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name

class MovieName(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name



class Cast(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name   




class Category(models.Model):
    Name = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Name        



class Year(models.Model):
    Year = models.CharField(max_length = 250 , default = 'NULL')
  

    def __str__(self):
        return self.Year        

class Songs(models.Model):
    SongName = models.CharField(max_length = 250 , default = 'NULL')
    Singer = models.ManyToManyField(Singer)
    MusicDirector = models.ManyToManyField(MusicDirector)
    Lyricist = models.ManyToManyField(Lyricist)
    MovieName = models.ForeignKey(MovieName, on_delete=models.CASCADE)
    Cast  = models.ManyToManyField(Cast)
    YoutubeLink = models.CharField(max_length = 250 , default = 'NULL')
    Category  = models.ForeignKey(Category, on_delete=models.CASCADE)
    # lyrics  = models.CharField(max_length = 250 , default = 'NULL')
    year  = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return self.SongName