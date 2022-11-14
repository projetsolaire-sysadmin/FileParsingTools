import sys
from app import fonctions_convert
import pandas as pd

# La classe class_EnedisSGEFormatParser permet de parser/formater un fichier ENEDIS 
# en un format exploitable par le Système Informatique d'Elance

class class_EnedisSGEFormatParser:
		
	def __init__(self, path_file):
		s=path_file.split('\\')
		self.path_file = path_file
		self.file = fonctions_convert.convert_argv_to_filename(s[len(s) - 1]) #le dernier
		self.lines = self.open_csv()
		self.afficher()
	
	def afficher(self):
		print("path_file :",self.path_file)
		print("file :",self.file)
		print("data :", self.lines[:5],"...")

	def open_csv(self):
		try:
			path_file = open(self.path_file, "r")
			lines = path_file.readlines()
			path_file.close()
			return lines
		except:
			print("class_EnedisSGEFormatParser error : problem when read the file (maybe filedoesn't exist) (add the path with'\\'")
			sys.exit(2)

	def parse(self):
	
		"""convertir lignes :"""
		#todo : pas horaire ou pas demi horaire ?
		#todo : W ou Wh ?
		# todo : arrondir la valeur
		# todo : recupere info fichier
		c=[]
		for line in self.lines:
			c.append(self.convertir_ligne(line))
		
		"""traitements"""
		#todo : supprimer derniere ligne vide
		#todo : supprimer entete en trop
		c = self.traitement_supprimer_entete_en_trop(c)
		# c = self.traitement_supprimer_derniere_ligne_vide(c)
		# print(c[0:5])
		
		"""conversion en dataframe pandas"""
		colonnes=["measurementDate","measurementHour","value"]
		df = pd.DataFrame(data=c,columns=colonnes)
		df = df.set_index('measurementDate')

		"""enregistrement en csv"""
		df.to_csv('output/'+self.file)


	def convertir_ligne(self,line):
		t=line.split(";")
		# for item in t:
		# 	print(item)

		#print(t[0])

		if t[0]!="ï»¿Identifiant PRM" and len(t[0])!=14 and t[0]!="Horodate" and not('E+' in t[0]):
			d= fonctions_convert.convert_ISOdate_to_date(t[0])
			u=[]
			u.append(fonctions_convert.convert_date_to_JJ_MM_AAAA(d))
			u.append(fonctions_convert.convert_date_to_HH_MM(d))
			u.append(t[1].strip()) #pour enlever le retour à la ligne
			#print(u)
			return u
		else:
			#il s'agit de l'entete
			return ["measurementDate","measurementHour","value"]
	
	def traitement_supprimer_entete_en_trop(self,c):
		#print("nombre de lignes : ",len(c))
		#print(c[0])
		for i in range(0,6):
			if c[0]==["measurementDate","measurementHour","value"]:
				del(c[0])
		# avec pandas, on ajoute les entetes après
		return c
	
	# def traitement_supprimer_derniere_ligne_vide(self,c):
	# 	print("traitement_supprimer_dernieres_lignes_vides : nombre de lignes : ",len(c))
	# 	print(c[len(c)-1])
	# 	# if c[i]==["","",""]:
	# 	# 	del(c[i])
	# 	print("traitement_supprimer_dernieres_lignes_vides : nombre de lignes : ",len(c))
	# 	return c





