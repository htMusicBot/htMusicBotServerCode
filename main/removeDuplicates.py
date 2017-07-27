import difflib


from models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song ,UserData

actor = Actor.objects.order_by('Name')

for i in len(actor):
	s = difflib.SequenceMatcher(None,a[i].Name,a[i+1].Name).ratio()
	if s >= 0.9:
		print a[i].Name + '  '  + a[i+1].Name
		# qs1.union(qs2, qs3)
