import sys

HEADERS_PRODUCTION_LIST = {'"",Month,Day,Hour,Energy Production [kWh]'}
HEADERS_CONSUMPTION_LIST = {'ï»¿date;value','ï»¿Identifiant PRM;Type de donnees;Date de debut;Date de fin;Grandeur physique;Grandeur metier;Etape metier;Unite;Pas en minutes'}

def main(argv):
	inputfile = get_inputfile(argv)
	FILE_TYPE = get_file_type(inputfile)
	if FILE_TYPE == "PRODUCTION_FILE_TYPE" :
		print("parse")
		# parser = EnedisEmailFormatParser()
		# parser.parse()
	elif FILE_TYPE == "CONSUMPTION_FILE_TYPE" :
		print("parse")
		# parser = EnedisSGEFormatParser()
		# parser.parse()


def get_inputfile(argv):
	# #infos
	# for arg in sys.argv:
	# 	print(arg)
	# print(len(sys.argv))
	# print(str(sys.argv))
	if(len(sys.argv)==2):
		#print(sys.argv[1])
		return sys.argv[1]
	else:
		print("input file missing (consumption or production file)")
		sys.exit(2)
	#parse_consumption()


def get_file_type(inputfile):
	#read header of the input file
	try:
		file = open(inputfile, "r")
		lines = file.readlines()
		file.close()
	except:
		print("problem when read the file (maybe filedoesn't exist) (add the path with'\\'")
		sys.exit(2)
	# for line in lines:
	# 	print(line.strip())
	# print("auto dectec:"+lines[0]+".")
	if str(lines[0]).strip() in HEADERS_PRODUCTION_LIST:
		print("production file detected")
		#parse production file
		return("PRODUCTION_FILE_TYPE")
	elif str(lines[0]).strip() in HEADERS_CONSUMPTION_LIST:
		print("consumption file detected")
		#parse consumption file
		return("CONSUMPTION_FILE_TYPE")
	else:
		print("production or consumtion file NOT detected. Add the next sentence in the good list :")
		print(lines[0])
		sys.exit(2)


if __name__ == "__main__":
	main(sys.argv[1:])




#decides what file format it is, and then is going to trigger the right script to parse it
# def autodetect():
#	 if (format is "EnedisEmailFormat") :
#		 parser = EnedisEmailFormatParser()
#		 parser.parse()
#	 else if (format is "EnedisSGEFormat") : 
#		 parser = EnedisSGEFormatParser()
#		 parser.parse()


#class EnedisEmailFormatParser:
#def open_csv():
#def parse():