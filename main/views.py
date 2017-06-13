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
from main.models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song


import urllib,urllib2,csv,requests,os,xlrd,string,re
from bs4 import BeautifulSoup
from requests import get
from io import open
import difflib

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
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print status.json()


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

                    if message_text.lower() in "hey,hi,supp,hello".split(','):
                        #messages sent when any user sends the first message
                        post_facebook_message(sender_id,'Hey! '+name + "this is your one stop solution for all your music cravings ")
                        post_facebook_message(sender_id , 'send us your craving in the following format and we will serve you the best we can . ')
                        post_facebook_message(sender_id,'#Songname *Singers $Actorsinsong !yourmood')
                        post_facebook_message(sender_id,'You can send all 4 or any one of them its up to you ')

                    else:
                        print "entered in else"
                        item = message_text.split(' ')
                        for x in item :
                            print "entered in for loop"

                            if '#' in x :
                                print "entered #"

                                SongName = x.split('#')[1]

                                post_facebook_message(sender_id,SongName)
                                # matches  = matching_algo(SongName , SongNameData)

                            elif '*' in x :
                                SongCast = x.split('*')[1]
                                singer = Singer.objects.exclude(Name = SongCast)
                                a = Song.objects.filter(Singer__in=singer)
                                print a.SongName

                                post_facebook_message(sender_id,a.SongName)
                                # matches  = matching_algo(SongCast , CastData)
                                
                            elif '$' in x :
                                Actors = x.split('$')[1]
                                post_facebook_message(sender_id,Actors)
                                # matches  = matching_algo(Actors , ActorsData)
                                
                            elif '!' in x :
                                Mood = x.split('!')[1]
                                post_facebook_message(sender_id,Mood)
                                # matches  = matching_algo(Mood , MoodData)    

                    
                    #message text is sent to the user
                    
                except Exception as e:
                    print e
                    pass

        return HttpResponse()  


#normal basic function to check the working of bot and to update the menu and get started text
def index(request):
    # CSVtoSQL()
    url_start="http://www.hindigeetmala.net//movie/2016.php?page=1"
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
        singer = Singer.objects.get_or_create(Name = item)[0]
        song.Singer.add(singer)


    allMusicDirector = tableRow[2].text
    musicDirectorArray = allMusicDirector.split(',')
    for item in musicDirectorArray:
        musicDirector = MusicDirector.objects.get_or_create(Name = item)[0]
        song.MusicDirector.add(musicDirector)



    allLyricist = tableRow[3].text
    lyricistArray = allLyricist.split(',')
    for item in lyricistArray:
        lyricist = Lyricist.objects.get_or_create(Name = item)[0]
        song.Lyricist.add(lyricist)


    allActor = tableRow[5].text
    musicActorArray = allActor.split(',')
    for item in musicActorArray:
        actor = Actor.objects.get_or_create(Name = item)[0]
        song.Cast.add(actor)


    allCategory = tableRow[6].text
    categoryArray = allCategory.split(',')
    for item in categoryArray:
        category = Category.objects.get_or_create(Name = item)[0]
        song.Category.add(category)


    movieName = MovieName.objects.get_or_create(Name = tableRow[4].text)[0]
    song.MovieName = movieName

    year11 = Year.objects.get_or_create(Year = year)[0]
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


































