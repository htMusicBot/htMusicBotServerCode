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

    # print tableRow[4].text.strip().split('(')[0]
    movieName = MovieName.objects.get_or_create(Name = tableRow[4].text.strip().split('(')[0])[0]

    song.MovieName = movieName

    year11 = Year.objects.get_or_create(Year = year.strip())[0]

    song.year = year11
    song.save()
    #print year11
    
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



    # year11.save()
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
