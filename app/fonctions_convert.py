from datetime import datetime, timedelta
import sys

def convert_ISOdate_to_date(s):
	if s[19:]=="+02:00" or s[19:]=="+01:00":
		s=s[:19]
		#print(s)
	else:
		print("error +02:00", s)
		sys.exit()
	d1 = datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")
	#print(type(d1), d1)
	return d1
	#ou .fromisoformat() https://stackoverflow.com/questions/17594298/date-time-formats-in-python

def convert_date_to_JJ_MM_AAAA(d):
	return datetime.strftime(d,"%d-%m-%Y")

def convert_date_to_HH_MM(d):
	return datetime.strftime(d,"%H:%M")

def convert_ElanceFormat_to_date(date, hour):
	return datetime.strptime(date+" "+hour,"%d-%m-%Y %H:%M")

def convert_ElanceFormat_to_date_heure_pleine(date, hour):
	d= datetime.strptime(date+" "+hour,"%d-%m-%Y %H:%M")
	# min = int(datetime.strftime(d,"%M"))
	return d - timedelta(minutes=float(datetime.strftime(d,"%M")))


def convert_argv_to_filename(str):
	if '\\' in str:  
		temp=str.split('\\')
		return temp[len(temp)-1]
	elif '/' in str:
		temp=str.split('/')
		return temp[len(temp)-1]
	else:
		return str


# d = datetime.datetime.now()
# print(d)
# print(convert_date_to_JJ_MM_AAAA(d))
# print(convert_date_to_HH_MM(d))	