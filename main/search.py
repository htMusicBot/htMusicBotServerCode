# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl importIndex DocType, Text, Date
# from elasticsearch.helpers import bulk
# from elasticsearch import Elasticsearch
# from . import models


# connections.create_connection()




# class SingerIndex(DocType):
#     Name = Text()
  




# class MusicDirectorIndex(DocType):
#     Name = Text()



# class ActorIndex(DocType):
#     Name = Text() 



# class LyricistIndex(DocType):
#     Name = Text()

# class MovieNameIndex(DocType):
#     Name = Text()
 




# class CategoryIndex(DocType):
#     Name = Text()     



# class YearIndex(DocType):
#     Year = Text()


# class SongIndex(DocType):
#     SongName = Text()
#     Singer = Text()
#     MusicDirector = Text()
#     Lyricist = Text()
#     MovieName = Text()
#     Cast  = Text()
#     YoutubeLink = Text()
#     Category = Text()
#     # Category  = models.ForeignKey(Category, on_delete=models.CASCADE, null = True)
#     # lyrics  = models.CharField(max_length = 250 , default = 'NULL')
#     year  = Text()



# class UserDataIndex(DocType):
#     Fbid = Text()
#     State = Text()
#     Cast  = Text()
#     Singer = Text()

#     Lyricist = Text()
#     MovieName = Text()
#     Category = Text()
#     # issue = models.CharField(max_length = 1000, default = 'NULL')
#     year  = Text()
#     query  = Text()

# def bulk_indexing():
#     BlogPostIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in models.Singer.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.MusicDirector.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.Actor.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.Lyricist.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.MovieName.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.Category.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.Year.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.Song.objects.all().iterator()))
#     bulk(client=es, actions=(b.indexing() for b in models.UserData.objects.all().iterator()))


# #############################################################################################################3

# from django.db import models

# from .search import SingerIndex , MusicDirectorIndex  , ActorIndex , LyricistIndex , MovieNameIndex , CategoryIndex ,YearIndex , SongIndex , UserDataIndex

# # Create your models here.



# class Singer(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

#     def indexing(self):
#        obj = SingerIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)



# class MusicDirector(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

#     def indexing(self):
#        obj = MusicDirectorIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)



# class Actor(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL' )
  

#     def indexing(self):
#        obj = ActorIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)



# class Lyricist(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

#     def indexing(self):
#        obj = LyricistIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)

# class MovieName(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
#     # MovieCast  = models.ManyToManyField(Actor)

  

#     def indexing(self):
#        obj = MovieNameIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)
 




# class Category(models.Model):
#     Name = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

#     def indexing(self):
#        obj = CategoryIndex(
#           meta={'id': self.id},
#           Name=self.Name,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)      



# class Year(models.Model):
#     Year = models.CharField(unique=True , max_length = 250 , default = 'NULL')
  

#     def indexing(self):
#        obj = YearIndex(
#           meta={'id': self.id},
#           Year=self.Year,
          
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)        

# class Song(models.Model):
#     SongName = models.CharField(max_length = 250 , default = 'NULL')
#     Singer = models.ManyToManyField(Singer, null = True)
#     MusicDirector = models.ManyToManyField(MusicDirector, null = True)
#     Lyricist = models.ManyToManyField(Lyricist, null = True)
#     MovieName = models.ForeignKey(MovieName, on_delete=models.CASCADE, null = True)
#     Cast  = models.ManyToManyField(Actor, null = True)
#     YoutubeLink = models.CharField(max_length = 250 , default = 'NULL', null = True)
#     Category = models.ManyToManyField(Category, null = True)
#     # Category  = models.ForeignKey(Category, on_delete=models.CASCADE, null = True)
#     # lyrics  = models.CharField(max_length = 250 , default = 'NULL')
#     year  = models.ForeignKey(Year, on_delete=models.CASCADE, null = True)

#     def indexing(self):
#        obj = SongIndex(
#           meta={'id': self.id},
#           SongName=self.SongName,
#           posted_date=self.posted_date,
#           title=self.title,
#           text=self.text
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)

# class UserData(models.Model):
#     Fbid = models.CharField(max_length = 250)
#     State = models.CharField(max_length = 250 , default = 'NULL')
#     Cast  = models.ManyToManyField(Actor, null = True)
#     Singer = models.ManyToManyField(Singer, null = True)

#     Lyricist = models.ManyToManyField(Lyricist, null = True)
#     MovieName = models.ForeignKey(MovieName, on_delete=models.CASCADE, null = True)
#     Category = models.ManyToManyField(Category, null = True)
#     # issue = models.CharField(max_length = 1000, default = 'NULL')
#     year  = models.ForeignKey(Year, on_delete=models.CASCADE, null = True)
#     query  = models.ManyToManyField(Song, null = True) 



#     def indexing(self):
#        obj = UserDataIndex(
#           meta={'id': self.id},
#           author=self.author.username,
#           posted_date=self.posted_date,
#           title=self.title,
#           text=self.text
#        )
#        obj.save()
#        return obj.to_dict(include_meta=True)




