from pymongo import MongoClient
import config, sys, json
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

counter -= 1
print counter, "/", num_vids

render = []
weekidx = 0
for weekday in punchcard:

	houridx = 0
	for hour in weekday:
		render.append([weekidx, houridx, weekday[houridx]])
		houridx += 1

	weekidx += 1

# write result to file
f = open("data.js", "w")
f.write("var data = " + json.dumps(render) + ";")  # python will convert \n to os.linesep
f.close()
