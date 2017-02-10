from pymongo import MongoClient
import config, sys
from datetime import datetime

# open mongodb connection
client = MongoClient(config.mongoDB())
db_name = "sailing-channels"
devMode = False

if len(sys.argv) != 2:
	db_name += "-dev"
	devMode = True
	print "*** DEVELOPER MODE ***"

db = client[db_name]

w, h = 24, 7;
punchcard = [[0 for x in range(w)] for y in range(h)]

vids = db.videos.find({}, projection=["publishedAt"])
num_vids = vids.count()
counter = 1

for vid in vids:
	dt = datetime.utcfromtimestamp(vid["publishedAt"])

	if counter % 100 == 0:
		print counter, "/", num_vids

	# upcount punchcard
	punchcard[dt.weekday()][dt.hour] += 1
	counter += 1

render = []
for weekday in punchcard:
	for hour in punchcard[weekday]:
		render.append([weekday, hour, punchcard[weekday][hour]])

print render
