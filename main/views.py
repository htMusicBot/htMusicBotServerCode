#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import csv
from main.models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song ,UserData


import urllib,urllib2,csv,requests,os,xlrd,string,re
from bs4 import BeautifulSoup
from requests import get
from io import open
import difflib
import random






#Some Global Variables goes here
year_arr=['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2000s','1990s','1980s','1970s','1960s','1950s','1940s','1930s']

#year_arr=['1980s','1970s','1960s','1950s','1940s','1930s']

base_url='http://www.hindigeetmala.net/'

song_count=1
# Create your views here.


VERIFY_TOKEN = 'musicBot'
PAGE_ACCESS_TOKEN = 'EAACCN4djHpkBAN7pazyZCHYSv14UPPYdUPCjmmbIFonmOR5we3mDrMTqYLJaByMjnD4LVjU0ZCZBCHgzsoeIGBgeldj3xULWYvoVAXHtufHoQaq4v0hN3GOxl4kvwmDgbkl7yqZCyCj74ZCbEiYMrpTpJM0AiAm0jJhZCnRTuqLwZDZD'


#function to extraxt data of the person who sens a message
def userdeatils(fbid):
    url = 'https://graph.facebook.com/v2.6/' + fbid + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAGE_ACCESS_TOKEN
    resp = requests.get(url=url)
    data =json.loads(resp.text)
    return data


#the message is sent from the page to the fbid associated to that message
def post_facebook_message(fbid,message_text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

    if message_text == 'singerQuickreply':
        response_msg = singerQuickreply(fbid)

    elif message_text == 'cards':
        response_msg = SongSearcher(fbid)     

    else:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})

    requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)


class MyChatBotView(generic.View):

    def get(self, request, *args, **kwargs):
        #verifying the token set
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Oops invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    
    #incomng message is decoded and various action are performed
    def post(self, request, *args, **kwargs):
        global sender_id
        incoming_message= json.loads(self.request.body.decode('utf-8'))
        print incoming_message

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                print message
                try:
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']
                    DataInstance = userdeatils(sender_id)
                    name = '%s %s'%(DataInstance['first_name'],DataInstance['last_name'])
                    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]


                    if message_text.lower() in "hey,hi,supp,hello".split(','):
                        #messages sent when any user sends the first message
                        post_facebook_message(sender_id,'Hey! '+ name + "  this is your one stop solution for all your music cravings ")
                        # post_facebook_message(sender_id , 'send us your craving in the following format and we will serve you the best we can . ')
                        # post_facebook_message(sender_id,'#Songname *Singers $Actorsinsong !yourmood')
                        # post_facebook_message(sender_id,'You can send all 4 or any one of them its up to you ')
                        post_facebook_message(sender_id,'singerQuickreply')

                    elif userInstance.State=='songName':
                        userInstance.State='NULL'
                        userInstance.save()
                        b = Song.objects.filter(SongName__contains = message_text) 
                        for item in b:

                            post_facebook_message(sender_id, item.SongName)
                        post_facebook_message(sender_id,'singerQuickreply')

                    elif userInstance.State=='singer':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = Singer.objects.filter(Name__contains = message_text)
                        print "singer name searched"
                        
                        # print b 
                        for item in a:
                            userInstance.Singer.add(item)
                        userInstance.save()
                        print "singer name saved to user data"

                        # SongSearcher(sender_id)
                        post_facebook_message(sender_id,'cards')

                        post_facebook_message(sender_id,'singerQuickreply')






                    elif userInstance.State=='lyricist':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = Lyricist.objects.filter(Name__contains = message_text)
                        # print a 
                        
                        # print b 
                        for item in a:
                            userInstance.Lyricist.add(item)
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        SongSearcher(sender_id)
                        post_facebook_message(sender_id,'singerQuickreply')

                    
                    elif userInstance.State=='movieName':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = MovieName.objects.filter(Name__contains = message_text)
                        print a
                        for item in a:
                            print "in movie loop "
                            print item
                            userInstance.MovieName = item
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # c = random.shuffle(b)
                        # post_facebook_message(sender_id,b[0].SongName)
                        SongSearcher(sender_id)
                        post_facebook_message(sender_id,'singerQuickreply')


                    elif userInstance.State=='cast':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = Actor.objects.filter(Name__contains = message_text)
                        # print a 
                        
                        # print b 
                        for item in a:
                            userInstance.Cast.add(item)
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        SongSearcher(sender_id)
                        post_facebook_message(sender_id,'singerQuickreply')

                    elif userInstance.State=='category':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = Category.objects.filter(Name__contains = message_text)
                        # print a 
                       
                        # print b 
                        for item in a:
                            userInstance.Category.add(item)
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # c = random.shuffle(b)
                        # post_facebook_message(sender_id,b[0].SongName)
                        SongSearcher(sender_id)
                        post_facebook_message(sender_id,'singerQuickreply')

                    elif userInstance.State=='year':
                        userInstance.State='NULL'
                        userInstance.save()
                        a = Year.objects.filter(Year__contains = message_text)
                        # print a 
                       
                        # print b
                        for item in a: 
                            userInstance.year = item
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        SongSearcher(sender_id)
                        post_facebook_message(sender_id,'singerQuickreply')

                    else:
                        print "entered in else"
                        item = message_text.split(' ')
                        for x in item :
                            print "entered in for loop"

                            if '#' in x :
                                print "entered #"

                                SongName = x.split('#')[1]
                                # singer = Singer.objects.exclude(Name = SongName)
                                print Songname
                                a = Song.objects.filter(SongName__contains =Songname)

                                print a[0].SongName

                                post_facebook_message(sender_id,a[0].SongName)
                                # matches  = matching_algo(SongName , SongNameData)

                            elif '*' in x :
                                SongCast = x.split('*')[1]
                                a = Singer.objects.filter(Name_contains=SongCast)

                                b = Song.objects.filter(Singer=a)
                                print b[0].SongName

                                post_facebook_message(sender_id,b[0].SongName)
                                # matches  = matching_algo(SongCast , CastData)
                                
                            elif '$' in x :
                                Actors = x.split('$')[1]
                                a = Actor.objects.filter(Name_contains=Actors)

                                b = Song.objects.filter(Cast=a)                             
                                post_facebook_message(sender_id,b[0].SongName)
                                # matches  = matching_algo(Actors , ActorsData)
                                
                            elif '!' in x :
                                category = x.split('!')[1]
                                a = Category.objects.filter(Name_contains=category)

                                b = Song.objects.filter(Category=a) 
                                post_facebook_message(sender_id,b[0].SongName)
                                # matches  = matching_algo(Mood , MoodData)    

                    
                    #message text is sent to the user
                    
                except Exception as e:
                    print e
                    pass



                try:
                    if 'quick_reply' in message['message']:
                        handle_quickreply(message['sender']['id'],
                        message['message']['quick_reply']['payload'])
                        return HttpResponse()
                    else:
                        pass
                except Exception as e:
                    print e
                    pass  

        return HttpResponse()  


#normal basic function to check the working of bot and to update the menu and get started text
def index(request):
    # CSVtoSQL()
    url_start="http://www.hindigeetmala.net//movie/2010.php?page=1"
    url_next=""
    url_curr=url_start
    while(url_start!=url_next):
        print "Scrapping for :"+url_curr
        GetMoviePageURL(url_curr)
        url_next=GetNextURL(url_curr)
        url_curr=url_next
        
    print "Completed Scrapping"
    return HttpResponse('Completed Scrapping')


def GetSongData(url,year):
    #print url
    url=url.replace(" ","%20")
    response = urllib2.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    #This one is for getting the song details
    table_songs_detail=soup.find("table",{"class": "b1 w760 pad2 allef"})
    row=[]

    # for item in table_songs_detail.findAll("td"):
    #     row.append(item.text)

    tableRow = table_songs_detail.findAll("td")

    song = Song.objects.get_or_create(SongName =tableRow[0].text)[0]

    allSinger = tableRow[1].text
    singerArray = allSinger.split(',')
    for item in singerArray:
        singer = Singer.objects.get_or_create(Name = item.strip())[0]
        song.Singer.add(singer)


    allMusicDirector = tableRow[2].text
    musicDirectorArray = allMusicDirector.split(',')
    for item in musicDirectorArray:
        musicDirector = MusicDirector.objects.get_or_create(Name = item.strip())[0]
        song.MusicDirector.add(musicDirector)



    allLyricist = tableRow[3].text
    lyricistArray = allLyricist.split(',')
    for item in lyricistArray:
        lyricist = Lyricist.objects.get_or_create(Name = item.strip())[0]
        song.Lyricist.add(lyricist)


    allActor = tableRow[5].text
    musicActorArray = allActor.split(',')
    for item in musicActorArray:
        actor = Actor.objects.get_or_create(Name = item.strip())[0]
        song.Cast.add(actor)


    allCategory = tableRow[6].text
    categoryArray = allCategory.split(',')
    for item in categoryArray:
        category = Category.objects.get_or_create(Name = item.strip())[0]
        song.Category.add(category)


    movieName = MovieName.objects.get_or_create(Name = tableRow[4].text.strip())[0]
    song.MovieName = movieName

    year11 = Year.objects.get_or_create(Year = year.strip())[0]
    song.year = year11
    
    #This one helps us in getting the embed url
    if(soup.find("iframe")):
        song_youtube_link=soup.find("iframe").get('src')

        # row.append(song_youtube_link)
        song.YoutubeLink = song_youtube_link        
    else:
        # row.append(" ")
        song.YoutubeLink = 'NULL'
    #This one is to get the lyrics
    # if(soup.find("pre")):
    #     song_lyrics=soup.find("pre").text.encode('utf8')
    #     song_lyrics=re.sub('[^a-zA-Z0-9-_*.\r\n ]', '', song_lyrics)
    #     row.append(song_lyrics)
    # else:
    #     row.append(" ")
    # checking for other table
    # if(soup.find("table",{"class","b1 allef w100p"})):
    #     table_meta=soup.find("table",{"class":"b1 allef w100p"})
    #     # checking for cast
    #     if(table_meta.find("td",{"itemprop":"actor"})):
    #         row.append(table_meta.find("td",{"itemprop":"actor"}).text)
    #     else:
    #         row.append(" ")
    #     #checking for director
    #     if(table_meta.find("td",{"itemprop":"director"})):
    #         row.append(table_meta.find("td",{"itemprop":"director"}).text)
    #     else:
    #         row.append(" ")
    #     #checking for producer
    #     if(table_meta.find("td",{"itemprop":"producer"})):
    #         row.append(table_meta.find("td",{"itemprop":"producer"}).text)
    #     else:
    #         row.append(" ")
    # else:
    #     row.append(" ")#empty for cast
    #     row.append(" ")#empty for director
    #     row.append(" ")#empty for producer  



    song.save()
    singer.save()
    musicDirector.save()    
    lyricist.save()
    movieName.save()
    actor.save()
    category.save()
    year11.save()

    return row
    

def GetSongPageURL(url,year):
    global song_count
    response = urllib2.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    table_songs_list=soup.find("table",{"class": "w760"})
    if(table_songs_list):
        for song in table_songs_list.findAll("td",{"class":"w185"}):
                song_link = song.find('a').get('href')
                song_url=base_url+song_link
                song_data=GetSongData(song_url,year)
                #Adding an ID for each song
                song_data.append(song_count)
                # song_data.append(year)
                print "Songs Written :"+str(song_count)
                song_count=song_count+1
                #print song_data[8][:10]
                #print type(song_data[8])
                #print len(song_data[8])

                # code to write into a csv file
                # with open('data.csv','ab') as f:
                #     writer = csv.writer(f)
                #     writer.writerows([song_data])
                #     f.close()
    return 0


def GetMoviePageURL(url):
    response = urllib2.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    table_arr=soup.find_all("table",{"class": "b1 w760 alcen"})
    year_arr=url.replace("http://www.hindigeetmala.net//movie/","")
    year_arr=year_arr.split(".")
    year=year_arr[0]
    #print table_arr
    for movie_row in table_arr[0].findAll("tr"):
        for movie in movie_row.findAll("td",{"class":"w25p h150"}):
            movie_link = movie.find('a').get('href')
            movie_url=base_url+movie_link
            GetSongPageURL(movie_url,year)

    return 0


def GetNextURL(url):
    response = urllib2.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    table_arr=soup.find("td",{"class": "vatop w140"})
    next_link = table_arr.find('a').get('href')
    next_url=base_url+'/movie/'+next_link
    return next_url


def matching_algo(input_string , data) :
    for item in data:

        a = []
        s = difflib.SequenceMatcher(None, item, input_string).ratio()
        a.append(s)


    for i in range(3):
        match = data[a.index(max(a))]
        matches = []
        matches.append(match)

        a.remove(max(a))

    return matches


def doubleParameterQuery(requests):
    # a = Song.objects.get(YoutubeLink = 'http://www.youtube.com/embed/b8t9TinNumE')
    singer = Singer.objects.exclude(Name = 'Krishna')
    category = Category.objects.exclude(Name = 'Rock Songs')
    a = Song.objects.exclude(Singer__in=singer).exclude(Category__in=category)
    print a
    return HttpResponse("hi")

def handle_quickreply(fbid,payload):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    output_text = 'Payload Recieved: ' + payload

    if payload == 'songName':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'songName'
        p.save()
        return post_facebook_message(fbid,'Enter song name')

    elif payload == 'singer':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'singer'
        p.save()
        return post_facebook_message(sender_id,'Enter singer name')

        
    elif payload == 'lyricist':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'lyricist'
        p.save()
        return post_facebook_message(sender_id,'Enter lyricist')
                
    elif payload == 'movieName':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'movieName'
        p.save()
        return post_facebook_message(sender_id,'Enter movie name')

    elif payload == 'cast':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'cast'
        p.save()
        return post_facebook_message(sender_id,'Enter actor/actress name')

    elif payload == 'category':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'category'
        p.save()
        return post_facebook_message(sender_id,'Enter category') 

    elif payload == 'year':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'year'
        p.save()
        return post_facebook_message(sender_id,'Enter year')  






def singerQuickreply(fbid):
    
    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":"Select your coloumn:",
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":"📽 Song Name",
                                "payload":"songName"
                              },
                              {
                                "content_type":"text",
                                "title":"🎤 Singer",
                                "payload":"singer"
                              },
                              {
                                "content_type":"text",
                                "title":"🎼 Lyricist",
                                "payload":"lyricist"
                              }, 
                              {
                                "content_type":"text",
                                "title":"🎞 Movie Name",
                                "payload":"movieName"
                              }, 
                              {
                                "content_type":"text",
                                "title":"🕴 Cast",
                                "payload":"cast"
                              }, 
                              {
                                "content_type":"text",
                                "title":"🌀 Mood/Category",
                                "payload":"category"
                              },
                              {
                                "content_type":"text",
                                "title":"⏳ Year",
                                "payload":"year"
                              }
                            ]
                          }
                        }
    return json.dumps(response_object)







def SongSearcher(sender_id):
    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]

    arraySinger =[]
    arrayYear =[]
    arrayCategory =[]
    arrayActor =[]
    arrayLyricist =[]
    arrayMovie =[]

    for item in userInstance.Singer.all():
        arraySinger.append(item.Name)

    # for item in userInstance.year.all():
    #     arrayYear.append(item.Name)
        
    for item in userInstance.Category.all():
        arrayCategory.append(item.Name)
        
    for item in userInstance.Cast.all():
        arrayActor.append(item.Name)
        
    for item in userInstance.Lyricist.all():
        arrayLyricist.append(item.Name)                  

    if userInstance.year:
        arrayYear.append(userInstance.year)
    else:
        pass    

    if userInstance.MovieName:
        arrayMovie.append(userInstance.MovieName)
        print  "Im if loop  = " + str(arrayMovie)


    else:
        pass          

    print "arrays of all parameters made"



    q = Singer.objects.filter(Name__in = arraySinger)

    print "entered singer "
    print "haha" + str(q)
    w = Year.objects.filter(Year = userInstance.year)
    print w
    print "entered year "
    y = MovieName.objects.filter(Name = userInstance.)
    print y
    print "entered movie "
    e = Category.objects.filter(Name__in = arrayCategory)
    print e
    print "entered category "

    r = Actor.objects.filter(Name__in = arrayActor)
    print r
    print "entered actor "
    t = Lyricist.objects.filter(Name__in = arrayLyricist)
    print t
    print "entered lyricist "

    if arraySinger:

        b = Song.objects.filter(Singer=q) 


    else :
        b =  Song.objects.exclude(Singer=q) 

    if arrayYear:

        z = b.filter(year=w) 


    else :
        z =  b.exclude(year=w)

    if arrayCategory:

        h = z.filter(Category=e) 


    else :
        h =  z.exclude(Category=e)

    if arrayActor :

        i = h.filter(Cast=r) 


    else :
        i =  h.exclude(Cast=r)

    if arrayLyricist :

        a = i.filter(Lyricist=t) 


    else :
        a =  i.exclude(Lyricist=t) 

    if arrayMovie :

        c = i.filter(MovieName=y) 


    else :
        c =  i.exclude(MovieName=y)       




    print "best best " + str(a)

    card_data2 = []
    print a 
    for i in a:
        print "entered loop"
        y = i.YoutubeLink
        # arraySinger = []
        x = y.split("/")
        print "x = " + str(x)
        song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"
        singerNames = ''
        for item in i.Singer.all():
            singerNames = singerNames + str(item) + ' , '


        
        
        card_data = {
                  "title": i.SongName,
                  "subtitle": singerNames,
                  "image_url": song_img,
                  
                  "buttons": [
                  {
                    "type": "postback",
                    "payload":"Ss" ,  
                    "title": "Play song"
                  },
                 
                  {
                    "type": "element_share"
                   }
                   ]
                   }

        card_data2.append(card_data) 
        print "cards appended"          

                    
    response_object = {
      "recipient": {
        "id": sender_id
      },
      "message": {
        "attachment": {
          "type": "template",
          "payload": {
            "template_type": "generic",
            "elements": card_data2
                }
            }
        }
    }

    print "response dumped"

    print json.dumps(response_object)

    # print response_object

    return json.dumps(response_object)


   

def cards(fbid, a ):



    card_data2 = []
    print a 
    for i in a:
        song_url = i.YoutubeLink
        # arraySinger = []
        x = song_url.split("https://www.youtube.com/embed/")
        song_img = "https://img.youtube.com/vi/" + x[1] + "/hqdefault.jpg"
        singerNames = ''
        for item in a.Singer.all():
            singerNames = singerNames + item + ' , '


        
        
        card_data = {
                  "title": i.SongName,
                  "subtitle": singerNames,
                  "image_url": song_img,
                  
                  "buttons": [
                  {
                    "type": "postback",
                    "payload":"ss" ,  
                    "title": "play song"
                  },
                  # {
                  #   "type": "web_url",
                  #   "url": i.menu_url,  
                  #   "title": "See Menu"
                  # },
                  {
                    "type": "element_share"
                   }
                   ]
                   }

        card_data2.append(card_data)           

                    
    response_object = {
      "recipient": {
        "id": fbid
      },
      "message": {
        "attachment": {
          "type": "template",
          "payload": {
            "template_type": "generic",
            "elements": card_data2
                }
            }
        }
    }

    print json.dumps(response_object)

    # print response_object

    return json.dumps(response_object)












