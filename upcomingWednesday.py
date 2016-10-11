import requests
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import json
import os

today = date.today()

def lastThursday(input):
    d = input.toordinal()
    last = d - 6
    sunday = last - (last % 7)
    thursday = sunday + 4
    return date.fromordinal(thursday)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

if today.weekday() == 2:
	#Fix this and find out why it doesnt work
	Wednesday = next_weekday(today, 2).strftime("%d-%m-%Y")
else:
	Wednesday = next_weekday(today, 2).strftime("%d-%m-%Y")

startDate = lastThursday(today).strftime("%d-%m-%Y")
currentDate = time.strftime("%Y-%m-%d")

headers = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1'}

payload1 = {
	'date_from': Wednesday,
	'date_to': Wednesday,
	'league%5B%5D': '',
	'orderby': 'date',
	'order_dir': 'asc',
	'action': 'lbs_api_client',
	'start': '0',
	'end': '1'
	}


r = requests.get('http://loughboroughsport.com/athletic-union/wp-admin/admin-ajax.php', headers=headers, params=payload1)
results = (r.text)

fixtureNumber = json.loads(results)['total']

payload2 = {
	'date_from': Wednesday,
	'date_to': Wednesday,
	'league%5B%5D': '',
	'orderby': 'start_time',
	'order_dir': 'asc',
	'action': 'lbs_api_client',
	'start': '0',
	'end': fixtureNumber
	}

r = requests.get('http://loughboroughsport.com/athletic-union/wp-admin/admin-ajax.php', headers=headers, params=payload2)
results = (r.text)


#print json.loads(results)['fixtures'][0]['team']

# Open a file
csvFile = open("Fixtures.txt", "wb")
reported = 0
missing = 0

ShowCaseReported = 0
ShowCaseMissing = 0

DDayReported = 0
DDayMissing = 0

BigMatchReported = 0
BigMatchMissing = 0


for i in json.loads(results)['fixtures']:
	#print [i][0]['result']
	if [i][0]['opposition'] != 'BYE' and [i][0]['opposition'] and [i][0]['home_away'] == '1' and [i][0]['venue']:
		reported += 1
		Sport = [i][0]['team']
		dateIn = [i][0]['start_date']
		dateIn = datetime.strptime(dateIn, "%Y-%m-%d").date()
		Date = dateIn.strftime("%A, %-d %B %Y")
		Round = [i][0]['round']
		start_time = [i][0]['start_time']
		AwayTeam = [i][0]['opposition']
		venue = [i][0]['venue']

		FinalString = start_time[:5] + ' - ' + Sport + ' vs ' + AwayTeam + ' - ' + venue + '\n'

		if [i][0]['home_away'] == '1':
			Home = 'TRUE'
			Away = 'FALSE'
			HomeTeam = 'Loughborough University'
			AwayTeam = [i][0]['opposition']
			HomeScore = [i][0]['for']
			AwayScore = [i][0]['against']
		elif [i][0]['home_away'] == '2':
			Home = 'FALSE'
			Away = 'TRUE'
			HomeTeam = [i][0]['opposition']
			AwayTeam = 'Loughborough University'
			HomeScore = [i][0]['against']
			AwayScore = [i][0]['for']
		else:
			Home = 'TRUE'
			Away = 'FALSE'
			HomeTeam = 'Loughborough University'
			AwayTeam = [i][0]['opposition']
			HomeScore = [i][0]['for']
			AwayScore = [i][0]['against']

		if Round.find("SHOWCASE") != -1:
			ShowCaseReported +=1
			Standard = 'FALSE'
			DDay = 'FALSE'
			DDayHome = 'FALSE'
			DDayAway = 'FALSE'
			Showcase = 'TRUE'
			BigMatch = 'FALSE'
		elif Round.find("D-Day") != -1:
			DDayReported +=1
			Standard = 'FALSE'
			DDay = 'TRUE'
			if Home == 'TRUE':
				DDayHome = 'TRUE'
				DDayAway = 'FALSE'
			else:
				DDayHome = 'FALSE'
				DDayAway = 'TRUE'
			Showcase = 'FALSE'
			BigMatch = 'FALSE'
		elif (Round.find("BIG") != -1) and (Round.find("MATCH") != -1):
			BigMatchReported +=1
			Standard = 'FALSE'
			DDay = 'FALSE'
			DDayHome = 'FALSE'
			DDayAway = 'FALSE'
			Showcase = 'FALSE'
			BigMatch = 'TRUE'
		else:
			Standard = 'TRUE'
			DDay = 'FALSE'
			DDayHome = 'FALSE'
			DDayAway = 'FALSE'
			Showcase = 'FALSE'
			BigMatch = 'FALSE'

		csvFile.write(FinalString);
		#print csv_line
		#print 'no result for ' + Sport


csvFile.close()
tempfixtures = open("Fixtures.txt", "r+")
lines = sorted(tempfixtures.readlines())
tempfixtures.seek(0)
tempfixtures.truncate()
tempfixtures.write('Wednesday Fixtures ' + Wednesday + '\n');
for g in lines:
	print(g)
	tempfixtures.write(g);
tempfixtures.close()




# TextWrap and centre
# from PIL import Image, ImageDraw, ImageFont
# import textwrap

# astr = '''The rain in Spain falls mainly on the plains.'''
# para = textwrap.wrap(astr, width=15)

# MAX_W, MAX_H = 200, 200
# im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
# draw = ImageDraw.Draw(im)
# font = ImageFont.truetype(
# 	'/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', 18)

# current_h, pad = 50, 10
# for line in para:
# 	w, h = draw.textsize(line, font=font)
# 	draw.text(((MAX_W - w) / 2, current_h), line, font=font)
# 	current_h += h + pad

# im.save('test.png')



