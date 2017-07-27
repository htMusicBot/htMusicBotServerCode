import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hateCrime.settings")
import django
django.setup()
from main.models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song ,UserData




def songQuery(sender_id):

    number = 0
    userInstance = UserData.objects.get(Fbid = sender_id)
    card_data2 = []

    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]

    arrayMovie = []

    allSinger = userInstance.Singer.all()
    print allSinger
    allCategory = userInstance.Category.all()
    allcast = userInstance.Cast.all()    
    allLyricist = userInstance.Lyricist.all()  
    allyear = userInstance.year.all()

    try:     
        arrayMovie.append(userInstance.MovieName)

    except Exception as e:

        print e
        pass   

    print "this is arraymovie" + str(arrayMovie)
    



    if allSinger:
        print "in singer "
        b = Song.objects.all()
        for item in allSinger:

            b = b.filter(Singer=item) 


    else :
        b =  Song.objects.exclude(Singer__in=allSinger)

    print "After sorting singers" 

    if allyear:
        print "yes in array year"


        z = b.filter(year__in=allyear) 

        # z = b
    else :
        # z =  b.exclude(year__in=allyear)
        z = b



    if allcast :
        i=z
        for item in allcast:


            i =i.filter(Cast=item) 


    else :
        i = z 


    print "After sorting actor"    
    

    if allLyricist :
        a=i
        for item in allcast:

            a = a.filter(Lyricist=item) 


    else :
        # a =  i.exclude(Lyricist__in=allLyricist) 
        a = i 
    print "After sorting Lyricist"     

    # print a    

    if userInstance.MovieName != None :
        print "entered array movie"

        j = a.filter(MovieName=userInstance.MovieName) 


    else :
        # c =  a.exclude(MovieName__in =) 
        j = a  

    print "After sorting Movie"      
    

    if allCategory :
        c=j
        for item in allCategory:

            c = c.filter(Category=item) 


    else :
        # a =  i.exclude(Lyricist__in=allLyricist) 
        c = j
    print "After sorting category" 

 




    print "best best " + str(c)

    return c 
    

