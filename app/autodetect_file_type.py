import sys
from app import class_EnedisSGEFormatParser, class_ConsumptionFile

HEADERS_PRODUCTION_LIST = {'"",Month,Day,Hour,Energy Production [kWh]'}
HEADERS_CONSUMPTION_LIST = {'ï»¿date;value',
	'ï»¿Identifiant PRM;Type de donnees;Date de debut;Date de fin;Grandeur physique;Grandeur metier;Etape metier;Unite;Pas en minutes',
	'Date de la mesure;Heure de la mesure;Valeur;Statut de la mesure;PRM;Type de données;Date de début;Date de fin;Grandeur métier;Grandeur physique;Statut demandé;Unité;Pas en minutes',
	'Date de la mesure;Heure de la mesure;Valeur;Statut de la mesure;PRM;Type de donnï¿½es;Date de dï¿½but;Date de fin;Grandeur mï¿½tier;Grandeur physique;Statut demandï¿½;Unitï¿½;Pas en minutes',
	'ï»¿Identifiant PRM;Type de donnees;Date de debut;Date de fin;Grandeur physique;Grandeur metier;Etape metier;Unite',
	'Identifiant PRM;Type de donnees;Date de debut;Date de fin;Grandeur physique;Grandeur metier;Etape metier;Unite;Pas en minutes'}
HEADERS_CONSUMPTION_PARSED_LIST ={"measurementDate,measurementHour,value"}


def detect(inputfile, option=''):#argv=sys.argv[1:]):
	#inputfile = get_inputfile(file)
	print(inputfile)
	FILE_TYPE = get_file_type(inputfile)
	if FILE_TYPE == "PRODUCTION_FILE_TYPE":
		print("parse")
		# parser = EnedisEmailFormatParser()
		# parser.parse()
	elif FILE_TYPE == "CONSUMPTION_FILE_TYPE":
		print("parse")
		parser = class_EnedisSGEFormatParser.class_EnedisSGEFormatParser(inputfile)
		parser.afficher()
		parser.parse()
		print(parser.file)
		q = class_ConsumptionFile.class_ConsumptionFile('output/' + parser.file)
		return q.file_formatted
		if option == 'option display graph': 
			q.graphique(option)
	elif FILE_TYPE == "CONSUMPTION_FILE_ALREADY_PARSED_TYPE" :
		q = class_ConsumptionFile.class_ConsumptionFile(inputfile)
		return q.file_formatted
		if option == 'option display graph': 
			q.graphique(option)
	elif FILE_TYPE == "CONSUMPTION_FILE_DAILY_TYPE" :
		print("consumption DAYS file detected, file not supported")
	elif FILE_TYPE == "NOT ENOUGH DATA" :
		print("Not enough data, file not supported")
	else:
		print("type file not detected")




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
	#  	print(line.strip())
	# print("auto dectec:"+lines[0]+".")
	
	#Vérification si fichier de données journalière
	for i in [1,2,3,4]:
		if 'Arrêté quotidien' in lines[i] or "ArrÃªtÃ© quotidien" in lines[i] :
			return("CONSUMPTION_FILE_DAILY_TYPE")
			
	if len(lines)<10:
		return "NOT ENOUGH DATA"

	if str(lines[0]).strip() in HEADERS_PRODUCTION_LIST:
		print("production file detected")
		#parse production file
		return("PRODUCTION_FILE_TYPE")
	elif str(lines[0]).strip() in HEADERS_CONSUMPTION_LIST:
		print("consumption file detected")
		#parse consumption file
		return("CONSUMPTION_FILE_TYPE")
	elif str(lines[0]).strip() in HEADERS_CONSUMPTION_PARSED_LIST:
		print("consumption file already parsed detected")
		return("CONSUMPTION_FILE_ALREADY_PARSED_TYPE")
	else:
		print("production or consumption file NOT detected. Add the next sentence in the good list :")
		print(lines[0])
		sys.exit(2)
		#TO DO : proposer d'ajouter le header dans la table de correspondance et d'identifier si prod ou conso !


if __name__ == "__main__":
	detect(sys.argv[1:])




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