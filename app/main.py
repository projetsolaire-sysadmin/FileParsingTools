import sys

# import pathlib
# print(pathlib.Path(__file__).parent.resolve())

from app import autodetect_file_type
import os
import datetime


def main(arg=""):

	if arg !="":
		file_path=arg
	elif(len(sys.argv)==2):
		file_path = sys.argv[1]
	else:
		print("input file missing (consumption or production file)")
		sys.exit(2)


	print("file_path",file_path)
	if file_path[len(file_path)-4:] ==".csv":
		#print(datetime.datetime.now())
		temp = autodetect_file_type.detect(file_path) #,'option display graph')
		print("\n fichier généré : ",temp,"\n")
		return temp
		print(datetime.datetime.now())
	else:
		dossier = file_path
		if os.path.exists(dossier):
			for file in os.listdir(dossier):
				print(file)
				return autodetect_file_type.detect(dossier + "\\" + file) #,'option display graph')
		else:
			print("erreur : le dossier n'existe pas ou le fichier n'est pas un csv")
			exit()


if __name__ == "__main__":
	main()
	




"""
options à dev :
calculer la qualité d'estimation ?
méthodes d'estimation
compléter l'année

If the implementation is hard to explain, it's a bad idea.

traiter un fichier déjà parsé : le détecter puis esquiver le parsing

j'ai beaucoup travailler sur les performances. au début : 104 sec. en optimisant le code, j'ai réussi à descendre à 20 secondes


DONE :
ajouter période manquante V2 car trop long (82 sec) : créer un dataframe avec date et copier valeur c'est peut-être plus rapide puis un join
-> -de 15 sec
"""