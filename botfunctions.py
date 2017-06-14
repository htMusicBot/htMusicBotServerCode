
import difflib

def bot():

	# x = ['#' , '*' , '$' , '!']

	x = message_text.split(' ')
	for item in x :
		if '#' in item :
			SongName = x.split('#')[1]
			matches  = matching_algo(SongName , SongNameData)

		elif '*' in item :
			SongCast = x.split('*')[1]
			matches  = matching_algo(SongCast , CastData)
			
		elif '$' in item :
			Actors = x.split('$')[1]
			matches  = matching_algo(Actors , ActorsData)
			
		elif '!' in item :
			Mood = Mood.split('!')[1]
			matches  = matching_algo(Mood , MoodData)


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






	







	










