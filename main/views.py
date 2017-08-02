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
# from fuzzywuzzy import fuzz
import random
import songScraper
from songQuery import songQuery
from templates import setMenu , greetingText , greetingButton
import datetime
# from dateutil import tz




import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#Some Global Variables goes here
year_arr=['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2000s','1990s','1980s','1970s','1960s','1950s','1940s','1930s']

#year_arr=['1980s','1970s','1960s','1950s','1940s','1930s']

base_url='http://www.hindigeetmala.net/'

song_count=1
# Create your views here.


VERIFY_TOKEN = 'musicBot'
PAGE_ACCESS_TOKEN = 'EAACCN4djHpkBAN7pazyZCHYSv14UPPYdUPCjmmbIFonmOR5we3mDrMTqYLJaByMjnD4LVjU0ZCZBCHgzsoeIGBgeldj3xULWYvoVAXHtufHoQaq4v0hN3GOxl4kvwmDgbkl7yqZCyCj74ZCbEiYMrpTpJM0AiAm0jJhZCnRTuqLwZDZD'


#function to extraxt data of the person who sends the message
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

        

    elif message_text == 'Category_quickreplies':
        response_msg = Category_quickreplies(fbid)    

    elif message_text == 'ACards':
        response_msg = afterSongQuickreply(fbid)

    elif message_text == 'yearQuickReply':
        response_msg = yearQuickreply(fbid)

    elif message_text == 'moreSongs':
        response_msg = moreSongs(fbid)
        # post_facebook_message(sender_id,'ACards') 

    elif message_text == 'randdom':
        response_msg = randomSongs(fbid) 

    elif message_text == 'afterSongSearcherQuickReply':
        response_msg = afterSongSearcherQuickReply(fbid)   
        

    else:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})

    requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)


def post_matching_quickreplies(fbid,message_text , data , input_string):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

   

    if message_text == 'matching_quickreplies':
        response_msg = matching_quickreplies(input_string, data ,fbid)
        print "above" + str(response_msg)    

    if message_text == 'songs_cards':
        response_msg = songs_cards(fbid ,data ,input_string )




    requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)         

# csvData = []
# def userArray(data):
#     csvData.append(data)
#     return csvData

def userCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="a.csv"'
    writer = csv.writer(response)
    # writer.writerow(data)
    print "data rendered to csv"
    return response


def userIneraction(sender_id , csvData):
    print "i am in user databse function"
    DataInstance = userdeatils(sender_id)
    extraData = DataInstance.values()
    sender_id = str(sender_id)
    extraData.append(sender_id)
    data = extraData + csvData

    timestamp  = datetime.datetime.now().strftime('%l:%M%p %Z on %b %d %Y')
    data.append(timestamp)
    print data
    data = map(unicode,data)

    print "i am in user databse function check 2"
    

    # with open('a.csv', 'a') as myfile:
    #     print "i am in user databse function check 3"
    #     wr = csv.writer(myfile)
    #     print "i am in user databse function check 4"
    #     wr.writerow(data)
    #     print "writing in csv done"
    with open('specificUsers/' + sender_id + '.csv', 'ab') as myfile:
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="a.csv"'
        writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        

        writer.writerow(data)

        print "data saved to csv"


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
                    firstName = '%s'%(DataInstance['first_name'])
                    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]
                    
                        


                    if message_text.lower() in "hey,hi,supp,hello".split(','):
                        print "entered in hi "
                    
                        #messages sent when any user sends the first message
                        textTemplate = ['Welcome %s, Nice to see you here :)'%firstName , 'Hey %s, Welcome to the Music Bot by Hindustan Times :)'%firstName , 'Hey %s! Get ready for some Bollywood nostalgia.'%firstName , 'Hi %s, here is your one-stop destination for Bollywood music. '%firstName, 'Hello, %s. In the mood for some Bollywood tunes?'%firstName , 'Hi %s, welcome to HT Music Bot. I have Bollywood tunes for you to brighten the day.'%firstName ]

                        a = random.choice(textTemplate)
                        print a
                        post_facebook_message(sender_id , str(a) )
                        userInstance.delete()
                        # post_facebook_message(sender_id , 'send us your craving in the following format and we will serve you the best we can . ')
                        # post_facebook_message(sender_id,'#Songname *Singers $Actorsinsong !yourmood')
                        # post_facebook_message(sender_id,'You can send all 4 or any one of them its up to you ')
                        post_facebook_message(sender_id,'singerQuickreply')

                    elif userInstance.State=='songName':
                        userInstance.State='NULL'
                        userInstance.save()
                        message_text = message_text.title()
                        # b = Song.objects.all().values()
                        b = Song.objects.select_related('SongName','YoutubeLink','Singer').all().values()
                      
                        print b
                        post_matching_quickreplies(sender_id, "songs_cards" ,b , message_text)
                        post_facebook_message(sender_id,'afterSongSearcherQuickReply')


                    elif userInstance.State=='singer':
                        userInstance.State='matchSinger'
                        userInstance.save()
                        message_text = message_text.title()

                        post_matching_quickreplies(sender_id , "matching_quickreplies" , Singer.objects.all() , message_text)

                    elif userInstance.State=='matchSinger':
                        userInstance.State='NULL'
                        userInstance.save()
                        message_text = message['message']['quick_reply']['payload']
                        a = Singer.objects.filter(Name = message_text)
                        print "singer name searched"
                        for item in a:
                            userInstance.Singer.add(item)
                        userInstance.save()
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')






                    elif userInstance.State=='lyricist':
                        userInstance.State='matchLyricist'
                        userInstance.save()
                        post_matching_quickreplies(sender_id , "matching_quickreplies" , Lyricist.objects.all() , message_text)
                        userInstance.save()

                    elif userInstance.State=='matchLyricist':
                        userInstance.State='NULL'
                        userInstance.save()
                        message_text = message['message']['quick_reply']['payload']
                        a = Lyricist.objects.filter(Name = message_text)
                        for item in a:
                            userInstance.Lyricist.add(item)
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')

                    
                    elif userInstance.State=='movieName':
                        userInstance.State='matchMovie'
                        userInstance.save()
                        message_text = message_text.title()
                        print "entered movies"
                        post_matching_quickreplies(sender_id , "matching_quickreplies" , MovieName.objects.all() , message_text)
                        # userInstance.save()

                    elif userInstance.State=='matchMovie':
                        userInstance.State='NULL'
                        print "entered matched movies"
                        print message_text
                        message_text = message['message']['quick_reply']['payload']
                        a = MovieName.objects.filter(Name = message_text)
                        print a
                        for item in a:
                            print "in movie loop "
                            print item
                            userInstance.MovieName = item
                        userInstance.save()
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')

                    elif userInstance.State=='cast':
                        userInstance.State='matchCast'
                        userInstance.save()
                        message_text = message_text.title()
                        post_matching_quickreplies(sender_id , "matching_quickreplies" , Actor.objects.all() , message_text)
                        

                    elif userInstance.State=='matchCast':
                        userInstance.State='NULL'
                        message_text = message['message']['quick_reply']['payload']
                        a = Actor.objects.filter(Name = message_text)
                        for item in a:
                            userInstance.Cast.add(item)
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')

                    elif userInstance.State=='category':
                        userInstance.State='NULL'
                        userInstance.save()
                        message_text = message_text.title()
                        # post_matching_quickreplies(sender_id , "matching_quickreplies" , Category.objects.all() , message_text)
                        a = Category.objects.filter(Name__contains = message_text)
                        # print a 
                       
                        # print b 
                        for item in a:
                            userInstance.Category.add(item)
                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # c = random.shuffle(b)
                        # post_facebook_message(sender_id,b[0].SongName)
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')

                    elif userInstance.State=='NULL':
                        pass


                    elif userInstance.State=='year':
                        userInstance.State='NULL'
                        userInstance.save()
                        payload = message['message']['quick_reply']['payload']
                        print payload
                        if payload=='1930s':
                            message_text = ['1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939']
                        elif payload=='1940s':
                            message_text = ['1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949']
                        elif payload=='1950s':
                            message_text = ['1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959']
                        elif payload=='1960s':
                            message_text = ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969']
                        elif payload=='1970s':
                            message_text = ['1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979']
                        elif payload=='1980s':
                            message_text = ['1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989']
                        elif payload=='1990s':
                            message_text = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999']
                        elif payload=='2000s':
                            message_text = ['2000','2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009']
                        elif payload=='2010s':
                            message_text = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
                        print message_text
                        print 'lalalalala'
                        a = Year.objects.filter(Year__in = message_text)
                        print a 
                       
                        # print b
                        for item in a: 
                            print 'la'
                            userInstance.year.add(item)

                        # userInstance.Singer.add(a[0])
                        userInstance.save()
                        # post_facebook_message(sender_id,b[0].SongName)
                        post_facebook_message(sender_id,'cards')
                        post_facebook_message(sender_id,'ACards')

                    
                    

                    else:
                        post_facebook_message(sender_id,'Looks like i lost you  please say hi and start a new conversation')
                        

                    
                except Exception as e:
                    print e
                    pass



                try:
                    if 'postback' in message:
                        if message['postback']['payload'] == 'STARTING123':
                            DataInstance = userdeatils(sender_id)
                            extraData = DataInstance.values()
                            sender_id = str(sender_id)
                            extraData.append(sender_id)
                            

                            timestamp  = datetime.datetime.now().strftime('%l:%M%p %Z on %b %d %Y')
                            extraData.append(timestamp)
                            data = map(unicode,extraData)
                            with open( 'usersRecord.csv', 'ab') as myfile:
                            # response = HttpResponse(content_type='text/csv')
                            # response['Content-Disposition'] = 'attachment; filename="a.csv"'
                                writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        

                                writer.writerow(extraData)

                            print "data saved to csv"
                            textTemplate = ['Welcome %s, Nice to see you here :)'%firstName , 'Hey %s, Welcome to the Music Bot by Hindustan Times :)'%firstName , 'Hey %s! Get ready for some Bollywood nostalgia.'%firstName , 'Hi %s, here is your one-stop destination for Bollywood music. '%firstName, 'Hello, %s. In the mood for some Bollywood tunes?'%firstName , 'Hi %s, welcome to HT Music Bot. I have Bollywood tunes for you to brighten the day.'%firstName ]
                            a = random.choice(textTemplate)
                            print a
                            p = UserData.objects.get_or_create(Fbid =sender_id)[0]
                            post_facebook_message(sender_id , str(a) )
                            post_facebook_message(sender_id,'singerQuickreply')
                            p.delete()
                    else:
                        pass
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
    url_start="http://www.hindigeetmala.net//movie/2016.php?page=2"
    url_next=""
    url_curr=url_start
    while(url_start!=url_next):
        print "Scrapping for :"+url_curr
        GetMoviePageURL(url_curr)
        url_next=GetNextURL(url_curr)
        url_curr=url_next
        
    print "Completed Scrapping"
    return HttpResponse('Completed Scrapping')


def doubleParameterQuery(requests):
    greetingText()
    greetingButton()
    return HttpResponse("hi")


def handle_quickreply(fbid,payload):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    output_text = 'Payload Recieved: ' + payload

    if payload == 'songName':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'songName'
        p.save()
        songText = ['Tell me which song you have on your mind' , 'Enter some lyrics from the song' , 'Do you remember the words? Tell me!' ]
        a = random.choice(songText)
        return post_facebook_message(fbid , str(a))

    elif payload == 'singer':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'singer'
        p.save()
        singerName = Singer.objects.all()
        singerName = sorted(singerName, key=lambda x: random.random())
        singerText = ['Enter the name of any singer' , 'Who’s voice do you want to listen to  ', 'Tell me which singer you would like to hear' ]
        a = random.choice(singerText)
        return post_facebook_message(sender_id,str(a) + ' like ' +  singerName[0].Name + ', ' + singerName[1].Name)

        
    elif payload == 'lyricist':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'lyricist'
        p.save()
        lyricistName = Lyricist.objects.all()
        lyricistName = sorted(lyricistName, key=lambda x: random.random())
        lyricistText = ['Enter the name of any lyricist' , 'Who’s your favourite lyricist? Tell me a name' , 'Which lyricist’s words would you like to hear']
        a = random.choice(lyricistText)
        return post_facebook_message(sender_id,str(a) + ' like ' + lyricistName[0].Name + ', ' + lyricistName[1].Name)
                
    elif payload == 'movieName':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'movieName'
        p.save()
        # movieName = MovieName.objects.all()
        # movieName = sorted(movieName, key=lambda x: random.random())
        movieText = ['Enter the name of any movie' , 'Is a song from a particular movie on your mind?'  , 'Which movie’s song would you like to hear now?' ]
        a = random.choice(movieText)
        # return post_facebook_message(sender_id,str(a) +' like  ' + movieName[0].Name + ', ' + movieName[1].Name)
        movieArray = ['3 Idiots','Gangs of Wasseypur','Rang De Basanti','Udaan','Lagaan','Taare Zameen Pe','Zindagi Na Milegi Dobara','Special 26','Bhaag Milkha Bhaag','Haider','Paan Singh Tomar','Queen','Barfi!','Baby','Chak de! India','My Name Is Khan','PK','Bajrangi Bhaijaan','Munna Bhai M.B.B.S.']
        name1 = random.choice(movieArray)
        name2 = random.choice(movieArray) 
        return post_facebook_message(sender_id,str(a) +' like ' + name1 + ', ' + name2)


    elif payload == 'cast':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'cast'
        p.save()
        # actor = Actor.objects.all()
        # actor = sorted(actor, key=lambda x: random.random())
        actorMale = ['Salman Khan', 'Shah Rukh Khan','Aamir Khan','Amitabh Bachchan','Dilip Kumar','Akshay Kumar','Ranbir Kapoor','Hrithik Roshan','Imran Khan','Ajay Devgn']
        male = random.choice(actorMale)
        actorFemale = ['Kangana Ranaut','Katrina Kaif','Deepika Padukone','Alia Bhatt','Priyanka Chopra','Sunny Leone','Kareena Kapoor Khan','Kriti Sanon','Shraddha Kapoor','Nargis Fakhri','Bipasha Basu','Sonakshi Sinha','Jacqueline Fernandez','Sonam Kapoor','Dia Mirza']
        female = random.choice(actorFemale)
        castText = [ 'Enter the name of any Bollywood actor or actress' , 'Are you looking for the songs of an actor or actress?' , 'Would you like to hear a song featuring your favourite actor' ]
        a = random.choice(castText)
        # return post_facebook_message(sender_id,str(a) + ' like  ' + actor[0].Name + ', ' + actor[1].Name)
        return post_facebook_message(sender_id,str(a) + ' like ' + male + ', ' + female)

    elif payload == 'category':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'category'
        p.save()
        return post_facebook_message(sender_id,'Category_quickreplies') 

    elif payload == 'year':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'year'
        p.save()
        return post_facebook_message(sender_id,'yearQuickReply')  

    elif payload == 'moreSongs':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'NULL'
        p.save()
        post_facebook_message(sender_id,'moreSongs')
        post_facebook_message(sender_id,'ACards')

    elif payload == 'filter':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.State = 'NULL'
        p.save()
        queryNull()
        return post_facebook_message(sender_id,'singerQuickreply') 

    elif payload == 'reset':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.delete()
        return post_facebook_message(sender_id,'singerQuickreply')

    elif payload == 'rondomSong':
        p = UserData.objects.get_or_create(Fbid =fbid)[0]
        p.delete()
        post_facebook_message(sender_id,'randdom')
        return post_facebook_message(sender_id,'singerQuickreply')


def singerQuickreply(fbid):

    filterText = ['Click on any of the options below to start' , 'What kind of songs would you like to listen to? Select any category to explore' , 'What songs do you like? Select options from the categories to help me find a song of your choice' , 'I have music to suit every mood. Pick options from the categories below' , 'Help me decide what songs to play for you. Select from these options' ]
    
    a = random.choice(filterText)
    
    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":str(a),
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":"🎞 Random Songs",
                                "payload":"rondomSong"
                              },
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
                                "title":"🕴 Actor/Actress",
                                "payload":"cast"
                              }, 
                              {
                                "content_type":"text",
                                "title":"🌀 Mood",
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


def afterSongQuickreply(fbid):
    afterOptionText = ['Do you want to hear more songs like this? Choose from these options' , 'What more can I play for you? Select options' , 'Add more filters to narrow down your search or start over.','Want to listen to something different? Choose from the options below' , 'Tell me what you want to hear now' , 'I can play something different for you. Help me by choosing from the options below']
    a = random.choice(afterOptionText)
     
    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":str(a),
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":"🎧 More Songs",
                                "payload":"moreSongs"
                              },
                              {
                                "content_type":"text",
                                "title":"🎬 Filter More",
                                "payload":"filter"
                              },
                              {
                                "content_type":"text",
                                "title":"🔰 Start Over",
                                "payload":"reset"
                              }
                            ]
                          }
                        }
    return json.dumps(response_object)


def SongSearcher(sender_id):
    card_data2 = []
    c = songQuery(sender_id)

    print c 

    c = sorted(c, key=lambda x: random.random())

    # random.shuffle(c)
    number = 0
    userdata = UserData.objects.get(Fbid = sender_id)
    if c:
        

            

            
        for i in c:
            print number
            print "entered loop"
            userdata.query.add(i) 
            if i.YoutubeLink != 'NULL':
                number = number + 1
                y = i.YoutubeLink
                # arraySinger = []
                x = y.split("/")
                print "x = " + str(x)
                song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"
                # singerNames = ''
                # for item in i.Singer.all():
                #     singerNames = singerNames + str(item) + ' , '



                card_data = {

                          "title": i.SongName,
                          # "subtitle": singerNames,
                          "image_url": song_img,
                          
                          "buttons": [
                          {
                            "type":"web_url",
                            "url":i.YoutubeLink,

                            # "url":"https://scontent.fdel8-1.fna.fbcdn.net/v/t34.0-12/19264885_1537111976319038_153011396_n.png?oh=754c80143d667a42a58350b5162f83ba&oe=59473531",
                            "title":"Play song",
                            "webview_height_ratio": "compact"
                          } ,
                         
                          {
                            "type": "element_share"
                           }
                           ]
                           }

                card_data2.append(card_data)
                

                print "cards appended"
            if number == 10:
                break



                   

                        
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

        optionText = ['Here are the closest matches. Hope you like these songs' , 'Hope this is what you were looking for. Enjoy!' , 'Based on what you told me, this is what I have found. Enjoy the music.' , 'Here’s what I found. Sing along to the songs of your choice!']


        options = random.choice(optionText)

        print 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        optionSelected = []
        y = UserData.objects.get(Fbid = sender_id)
        # print y
        aa = y.Cast.all()
        print str(aa) + 'iiii'
        # a = Actor.objects.filter(Name = aa[0].Name)
        # print a
        if aa:
            cast = ''
            for item in range(len(aa)):
                a = aa[item].Name
                cast = cast + str(a) + ', '
            a = 'Cast: ' + str(cast)
            optionSelected.append(a)
        print 'hhiiii'


        bb = y.Singer.all()
        if bb :
            singer = ''
            for item in range(len(bb)):
                a = bb[item].Name
                singer = singer + str(a) + ','
            b = 'Singer: ' + str(singer)
            optionSelected.append(b)


        cc = y.Lyricist.all()
        if cc :
            lyricist = ''
            for item in range(len(cc)):
                a = cc[item].Name
                lyricist = lyricist + str(a) + ','
            c = 'Lyricist: ' + str(lyricist)
            optionSelected.append(c)

        # d = MovieName.objects.filter(Name__in = y.MovieName)
        d = y.MovieName
        print d
        if d :
            dd = 'Movie Name:' + str(d)
            optionSelected.append(dd)

        ee = y.Category.all()
        if ee:
            category = ''
            for item in range(len(ee)):
                a = ee[item].Name
                category = category + str(a) + ','
            e = 'Category: ' + str(category)
            optionSelected.append(e)


        ff = y.year.all()
        if ff:
            year = [] 
            for item in range(len(ff)):
                a = int(ff[item].Year)
                print a
                year.append(a)
            maxYear = max(year)
            minYear = min(year)
            f = 'Year: ' + str(minYear) + '-' + str(maxYear)
            optionSelected.append(f)


        
        print 'array aagaye'
        print optionSelected
        userIneraction(sender_id,optionSelected)
        selectedOtions = ''
        for i in optionSelected:
            if optionSelected.index(i) == len(optionSelected) - 1:
                a = i.replace(',', '')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a)
            else:
                a = i.replace(',', '')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a) + '; '

        selectedOtions = " ".join(selectedOtions.split())






        
        moreFiltersOptions = ['You had selected %s.'%selectedOtions , 'You chose %s.'%selectedOtions]
        filerOptions = random.choice(moreFiltersOptions)
        post_facebook_message(sender_id,str(options))

        post_facebook_message(sender_id,str(filerOptions))    

        return json.dumps(response_object)

    else: 
        post_facebook_message(sender_id,"sorry according to your filters couldint find an appropriate match") 
            
 
def matching_quickreplies(input_string , data , sender_id) :
    
    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]
    w =0
    quickreply_array = [] 
    for item in data:
        realName  =item.Name
        if input_string.lower() in realName.lower():
            print item.Name


            

            quickreply_data = {
                                "content_type":"text",
                                "title":item.Name,
                                "payload":item.Name
                              }

            quickreply_array.append(quickreply_data)
            print "this is input string quickreply array" + str(quickreply_array)



            w = w+1

            if w==3:
                break;






    if not quickreply_array:
        a = []
        for item in data.exclude(Name  = ''):
            print "i am first name data" + str(item.Name)

             # s = fuzz.ratio(item.Name, input_string)
            realName  =item.Name
            print realName.split()[0]
            s = difflib.SequenceMatcher(None, realName.lower().split()[0], input_string.lower().split()[0]).ratio()
            a.append(s)
            # print s 

            # print a     

        # matches = []
        
        print a    
        for i in range(3):

            if max(a)>0.8:
                print "this is max ratio" + str(max(a))

                match = data[a.index(max(a))].Name
                

                # matches.append(match)

                a.remove(max(a))

                print match
                quickreply_data = {
                                    "content_type":"text",
                                    "title":match,
                                    "payload":match
                                  }

                quickreply_array.append(quickreply_data)

        

        
                # post_facebook_message(sender_id,match)
                w = w+1
                print "debugging  " + str(w)
                print "this is matched quickreply array" + str(quickreply_array)
                
                # if w==3:
                #     break
        if not quickreply_array:
            a = []
            for item in data.exclude(Name  = ''):
                print "i am last name data" + str(item.Name)

                 # s = fuzz.ratio(item.Name, input_string)
                realName  =item.Name
                # print realName.split()
                nameArray = realName.split()
                if len(nameArray)>1:
                    s = difflib.SequenceMatcher(None, realName.lower().split()[1], input_string.lower().split()[0]).ratio()
                    a.append(s)

                else:  

                    a.append(0)  
            # print s 

            # print a     

        # matches = []
        
            print a    
            for i in range(3):


                if max(a)>0.8:
                    print "this is max ratio" + str(max(a))
                    print a.index(max(a))

                    match = data[a.index(max(a))].Name
                    

                    # matches.append(match)

                    a.remove(max(a))

                    print match
                    quickreply_data = {
                                        "content_type":"text",
                                        "title":match,
                                        "payload":match
                                      }

                    quickreply_array.append(quickreply_data)

            

            
                    # post_facebook_message(sender_id,match)
                    w = w+1
                    print "debugging  " + str(w)
                    print "this is matched quickreply array" + str(quickreply_array)



    else :
        pass         



    if w==0 :
                print "no match found" 
                userInstance.State='NULL'
                userInstance.save()
                post_facebook_message(sender_id,"No matches found") 
                post_facebook_message(sender_id,"singerQuickreply")   
                print "this is array " + str(quickreply_array)
               


    elif len(quickreply_array) == 1:
        print "entered len array loop"


        if userInstance.State=='matchSinger':
            userInstance.State='NULL'
            userInstance.save()
            message_text = quickreply_array[0]['payload']
            a = Singer.objects.filter(Name= message_text)
            print "singer name searched"
            for item in a:
                userInstance.Singer.add(item)
            userInstance.save()
            post_facebook_message(sender_id,'cards')
            post_facebook_message(sender_id,'ACards')


        elif userInstance.State=='matchLyricist':
            userInstance.State='NULL'
            userInstance.save()
            message_text = quickreply_array[0]['payload']
            a = Lyricist.objects.filter(Name= message_text)
            for item in a:
                userInstance.Lyricist.add(item)
            # userInstance.Singer.add(a[0])
            userInstance.save()
            # post_facebook_message(sender_id,b[0].SongName)
            post_facebook_message(sender_id,'cards')
            post_facebook_message(sender_id,'ACards')

        elif userInstance.State =='matchMovie':
            print "entered match movie loop "
            userInstance.State='NULL'
            print "entered matched movies"
            # print message_text
            message_text = quickreply_array[0]['payload']
            a = MovieName.objects.filter(Name= message_text)
            print a
            for item in a:
                print "in movie loop "
                print item
                userInstance.MovieName = item
            userInstance.save()
            post_facebook_message(sender_id,'cards')
            post_facebook_message(sender_id,'ACards')
            

        elif userInstance.State=='matchCast':
            userInstance.State='NULL'
            message_text = quickreply_array[0]['payload']
            a = Actor.objects.filter(Name= message_text)
            for item in a:
                userInstance.Cast.add(item)
            userInstance.save()
            # post_facebook_message(sender_id,b[0].SongName)
            post_facebook_message(sender_id,'cards')
            post_facebook_message(sender_id,'ACards')
                
    else:
        response_object =   {
                                        "recipient":{
                                          "id":sender_id
                                      },
                                      "message":{
                                        "text":"Did you mean?",
                                        "quick_replies":quickreply_array
                                      }
                                    }

            # print response_object


        x = json.dumps(response_object)    

        print x   

        return x


def songs_cards(sender_id , data , input_string):
    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]

    a = []
    card_data2 = []
    w = 0
    for i in data:
        if input_string.lower() in i['SongName'].lower():
            print i['SongName']


            if i['YoutubeLink'] != 'NULL':
                y = i['YoutubeLink']
                x = y.split("/")
                print "x = " + str(x)
                song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"
                # singerNames = ''
                # for item in i['Singer']:
                #     singerNames = singerNames + str(item) + ' , '
                card_data = {
                      "title": i['SongName'],
                      # "subtitle": i['Singer'],
                      "image_url": song_img,
                      
                      "buttons": [
                      {
                        "type":"web_url",
                        "url":i['YoutubeLink'],

                        # "url":"https://scontent.fdel8-1.fna.fbcdn.net/v/t34.0-12/19264885_1537111976319038_153011396_n.png?oh=754c80143d667a42a58350b5162f83ba&oe=59473531",
                        "title":"Play song",
                        "webview_height_ratio": "compact"
                      } ,
                     
                      {
                        "type": "element_share"
                       }
                       ]
                       }

                card_data2.append(card_data)

                w = w+1

            if w==10:
                break;

    if not card_data2:   
        for i in data.iterator():
            s = difflib.SequenceMatcher(None, i['SongName'], input_string).ratio()
            a.append(s)

        for item in range(50):
            if max(a)>0.5:

                print "this is max ratio" + str(a.index(max(a)))

                i = data[a.index(max(a))]
                
                a.remove(max(a))

                if i['YoutubeLink'] != 'NULL':
                    y = i['YoutubeLink']
                    x = y.split("/")
                    print "x = " + str(x)
                    song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"
                    # singerNames = ''
                    # for item in i['Singer']:
                    #     singerNames = singerNames + str(item) + ' , '
                    card_data = {
                          "title": i['SongName'],
                          # "subtitle": i['Singer'],
                          "image_url": song_img,
                          
                          "buttons": [
                          {
                            "type":"web_url",
                            "url":i['YoutubeLink'],

                            # "url":"https://scontent.fdel8-1.fna.fbcdn.net/v/t34.0-12/19264885_1537111976319038_153011396_n.png?oh=754c80143d667a42a58350b5162f83ba&oe=59473531",
                            "title":"Play song",
                            "webview_height_ratio": "compact"
                          } ,
                         
                          {
                            "type": "element_share"
                           }
                           ]
                           }

                    card_data2.append(card_data)

                    w = w+1
                    if w == 10:
                        break

                    print "cards appended"   
            elif w == 10:
                break

    else :
        pass         



    if w==0 :
                print "no match found" 
                userInstance.State='NULL'
                userInstance.save()
                post_facebook_message(sender_id,"No matches found") 
                post_facebook_message(sender_id,"singerQuickreply")                   

    
    else:                    
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

        optionText = ['Here are the closest matches. Hope you like these songs' , 'Hope this is what you were looking for. Enjoy!' , 'Based on what you told me, this is what I have found. Enjoy the music.' , 'Here’s what I found. Sing along to the songs of your choice!']

        options = random.choice(optionText)

        print 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        optionSelected = []
        y = UserData.objects.get(Fbid = sender_id)
        # print y
        aa = y.Cast.all()
        print str(aa) + 'iiii'
        # a = Actor.objects.filter(Name = aa[0].Name)
        # print a
        if aa:
            cast = ''
            for item in range(len(aa)):
                a = aa[item].Name
                cast = cast + str(a) + ','
            a = 'Cast: ' + str(cast)
            optionSelected.append(a)
        print 'hhiiii'


        bb = y.Singer.all()
        if bb :
            singer = ''
            for item in range(len(bb)):
                a = bb[item].Name
                singer = singer + str(a) + ','
            b = 'Singer: ' + str(singer)
            optionSelected.append(b)


        cc = y.Lyricist.all()
        if cc :
            lyricist = ''
            for item in range(len(cc)):
                a = cc[item].Name
                lyricist = lyricist + str(a) + ','
            c = 'Lyricist: ' + str(lyricist)
            optionSelected.append(c)

        # d = MovieName.objects.filter(Name__in = y.MovieName)
        d = y.MovieName
        print d
        if d :
            dd = 'Movie Name:' + str(d)
            optionSelected.append(dd)

        ee = y.Category.all()
        if ee:
            category = ''
            for item in range(len(ee)):
                a = ee[item].Name
                category = category + str(a) + ','
            e = 'Category: ' + str(category)
            optionSelected.append(e)


        ff = y.year.all()
        if ff:
            year = [] 
            for item in range(len(ff)):
                a = int(ff[item].Year)
                print a
                year.append(a)
            maxYear = max(year)
            minYear = min(year)
            f = 'Year: ' + str(minYear) + '-' + str(maxYear)
            optionSelected.append(f)


        print 'array aagaye'
        print optionSelected
        userIneraction(sender_id,optionSelected)
        selectedOtions = ''
        for i in optionSelected:
            if optionSelected.index(i) == len(optionSelected) - 1:
                a = i.replace(',', '')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a)
            else:
                a = i.replace(',', '')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a) + '; '

        selectedOtions = " ".join(selectedOtions.split())

            
        moreFiltersOptions = ['You had selected %s.'%selectedOtions , 'You chose %s.'%selectedOtions]
        filerOptions = random.choice(moreFiltersOptions)
        post_facebook_message(sender_id,str(options))

        post_facebook_message(sender_id,str(filerOptions)) 

        return json.dumps(response_object)
        

def Category_quickreplies(sender_id):
    

    card_data2 = []
    c = songQuery(sender_id)
    print c 

    number = 0
    categoryArray = []
    # counter = 0
    c  = c[::-1]

    for i in c:
        print "this is i = " + str(i)
        # print c[]

        
        category = i.Category.all()
        for item in category:
            # print item 
            if item.Name != '':
                print "entered"
                categoryArray.append(item.Name)
                print item 


        if len(categoryArray) == 10:
            break


        print "this is categoryArray"  + str(categoryArray)


    x = list(set(categoryArray))
    print "jojojoj" + str(x)

    random.shuffle(x)
    print "hihihi" + str(x) 
    x = filter(None, x)

    for item in x:
        number = number + 1
        print number
            

        


    
    
        quickreply_array ={
                                "content_type":"text",
                                "title":item,
                                "payload":item
                              }



        card_data2.append(quickreply_array) 
        print "cards appended"   
        if number == 10:
            break       

    
    moodText = ['What kind of songs are you looking for?' , 'Tell me what kind of music you want right now. Choose from these options' , 'I’ll find music that suits your current mood. Tell me what you want to hear' ]
    a = random.choice(moodText)
    response_object =  {
                            "recipient":{
                              "id":sender_id
                          },
                          "message":{
                            "text":str(a),
                            "quick_replies":card_data2
                          }
                        }

    print "response dumped"

    print json.dumps(response_object)

    return json.dumps(response_object)


def yearQuickreply(fbid):
    array = ['1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s','2010s']
    yearText = ['In the mood for golden oldies or the latest hits? Choose from these options ', 'Are you looking for music from a particular era?' , 'I can find you music from a specific decade. Tell me what you want to hear']
    a = random.choice(yearText)
    card_data2 = []
    for item in array:
        quickreply_array = {
                        "content_type":"text",
                        "title":item,
                        "payload":item
                       }
        card_data2.append(quickreply_array) 
    

    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":str(a),
                            "quick_replies":card_data2
                          }
                        }
    return json.dumps(response_object)


def moreSongs(sender_id):
    userInstance = UserData.objects.get(Fbid = sender_id)
    
    c = songQuery(sender_id)
    number = 0     

    array = userInstance.query.all().values_list('SongName')
    array = c.exclude(SongName__in = array)
    card_data2 = []


    
    if array:
        for i in array:
            print number
            print "entered loop"
            userInstance.query.add(i)
            if i.YoutubeLink != 'NULL':
                number = number + 1
                y = i.YoutubeLink
                # arraySinger = []
                x = y.split("/")
                print "x = " + str(x)
                song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"
                # singerNames = ''
                # for item in i.Singer.all():
                #     singerNames = singerNames + str(item) + ' , '
                card_data = {

                          "title": i.SongName,
                          # "subtitle": singerNames,
                          "image_url": song_img,
                          
                          "buttons": [
                          {
                            "type":"web_url",
                            "url":i.YoutubeLink,

                            # "url":"https://scontent.fdel8-1.fna.fbcdn.net/v/t34.0-12/19264885_1537111976319038_153011396_n.png?oh=754c80143d667a42a58350b5162f83ba&oe=59473531",
                            "title":"Play song",
                            "webview_height_ratio": "compact"
                          } ,
                         
                          {
                            "type": "element_share"
                           }
                           ]
                           }

                card_data2.append(card_data)
                 
                if number == 10:
                    break



                print "cards appended"
            if number == 10:
                break



                   

                        
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
        optionText = ['Here are the closest matches. Hope you like these songs' , 'Hope this is what you were looking for. Enjoy!' , 'Based on what you told me, this is what I have found. Enjoy the music.' , 'Here’s what I found. Sing along to the songs of your choice!']


        options = random.choice(optionText)

        print 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        optionSelected = []
        y = UserData.objects.get(Fbid = sender_id)
        # print y
        aa = y.Cast.all()
        print str(aa) + 'iiii'
        # a = Actor.objects.filter(Name = aa[0].Name)
        # print a
        if aa:
            cast = ''
            for item in range(len(aa)):
                a = aa[item].Name
                cast = cast + str(a) + ','
            a = 'Cast: ' + str(cast)
            optionSelected.append(a)
        print 'hhiiii'


        bb = y.Singer.all()
        if bb :
            singer = ''
            for item in range(len(bb)):
                a = bb[item].Name
                singer = singer + str(a) + ','
            b = 'Singer: ' + str(singer)
            optionSelected.append(b)


        cc = y.Lyricist.all()
        if cc :
            lyricist = ''
            for item in range(len(cc)):
                a = cc[item].Name
                lyricist = lyricist + str(a) + ','
            c = 'Lyricist: ' + str(lyricist)
            optionSelected.append(c)

        # d = MovieName.objects.filter(Name__in = y.MovieName)
        d = y.MovieName
        print d
        if d :
            dd = 'Movie Name:' + str(d)
            optionSelected.append(dd)

        ee = y.Category.all()
        if ee:
            category = ''
            for item in range(len(ee)):
                a = ee[item].Name
                category = category + str(a) + ','
            e = 'Category: ' + str(category)
            optionSelected.append(e)


        ff = y.year.all()
        if ff:
            year = [] 
            for item in range(len(ff)):
                a = int(ff[item].Year)
                print a
                year.append(a)
            maxYear = max(year)
            minYear = min(year)
            f = 'Year: ' + str(minYear) + '-' + str(maxYear)
            optionSelected.append(f)

        
        print optionSelected
        userIneraction(sender_id,optionSelected)
        selectedOtions = ''
        for i in optionSelected:
            if optionSelected.index(i) == len(optionSelected) - 1:
                a = i.replace(',', ' ')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a)
            else:
                a = i.replace(',', '')
                # selectedOtions = str(selectedOtions).strip()
                selectedOtions = selectedOtions + str(a) + '; '

        selectedOtions = " ".join(selectedOtions.split())


        
        moreFiltersOptions = ['You had selected %s.'%selectedOtions , 'You chose %s '%selectedOtions]
        filerOptions = random.choice(moreFiltersOptions)
        post_facebook_message(sender_id,str(options))

        post_facebook_message(sender_id,str(filerOptions))     
    

        print "response dumped"

        print json.dumps(response_object)

        # print response_object

        return json.dumps(response_object)

    else:
        post_facebook_message(sender_id,"Sorry there are no more songs ")  
        userInstance.State='NULL'
        userInstance.save()

        # post_facebook_message(sender_id,'singerQuickreply')    


def queryNull():
    userdata = UserData.objects.get(Fbid = sender_id)

    array = userdata.query.all()
    if array:
        for i in array:
            userdata.query.remove(i)


    else:
        pass


def check(requests):
    actor = Lyricist.objects.order_by('Name')

    for i in range(len(actor)):
        s = difflib.SequenceMatcher(None,actor[i].Name,actor[i+1].Name).ratio()
        if s >= 0.9:
            # b = Actor.objects.filter(Name=actor[i].Name)[0]
            # print b.Name = 
            # b.add(actor[i+1])
            # Actor.objects.filter(Name=actor[i+1].Name).delete()
            # a1 = actor[i].Name
            # a2 = actor[i+1].Name
            # aa = chain(a1,a2)
            # print aa
            # b.Name = aa
            # c = Actor.objects.filter(Name=actor[i].Name)[0]
            # c.delete()
            # print str(s)
            # with open(filename, 'wb') as f:
            #     writer = csv.writer(f)
            #     writer.writerow((actor[i].Name , actor[i+1].Name , str(s)))
            print actor[i].Name + ',' + actor[i+1].Name + ',' + str(s)
            # + ',' + str(s)


def randomSongs(sender_id):
    randomSongs = Song.objects.all()
    number = 0
    card_data2 = []
    for item in range(100):
        if number <= 10:
            i = random.choice(randomSongs)
            print "entered loop"
            if i.YoutubeLink != 'NULL':
                number = number +1
                y = i.YoutubeLink
                x = y.split("/")
                print "x = " + str(x)
                song_img = "https://img.youtube.com/vi/" + x[-1] + "/hqdefault.jpg"

                card_data = {

                          "title": i.SongName,
                          "image_url": song_img,
                          
                          "buttons": [
                          {
                            "type":"web_url",
                            "url":i.YoutubeLink,
                            "title":"Play song",
                            "webview_height_ratio": "compact"
                          } ,
                         
                          {
                            "type": "element_share"
                           }
                           ]
                           }

                card_data2.append(card_data)
                

                print "cards appended"

        if number == 10:
            break
                    
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

    return json.dumps(response_object)

        
def afterSongSearcherQuickReply(fbid):
    afterOptionText = ['Do you want to hear more songs like this? Choose from these options' , 'What more can I play for you? Select options' , 'Add more filters to narrow down your search or start over.','Want to listen to something different? Choose from the options below' , 'Tell me what you want to hear now' , 'I can play something different for you. Help me by choosing from the options below']
    a = random.choice(afterOptionText)
     
    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":str(a),
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":"🎬 Filter More",
                                "payload":"filter"
                              },
                              {
                                "content_type":"text",
                                "title":"🔰 Start Over",
                                "payload":"reset"
                              }
                            ]
                          }
                        }
    return json.dumps(response_object)



