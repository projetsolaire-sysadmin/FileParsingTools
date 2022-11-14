import sys
from app import fonctions_convert
import numpy as np
import pandas as pd
from datetime import datetime
import math

# La classe class_ConsumptionFile permet de formater le fichier (compléter les données)

#option de développement :
TEST_SAUVEGARDER_CSV_INTERMEDIAIRE = False


class class_ConsumptionFile:
	
	def __init__(self, file):
		self.file = file
		if '\\' in file: s=file.split('\\')
		if "/" in file:	 s=file.split('/')
		self.filename=s[len(s)-1] #le dernier
		try:
			self.df = pd.read_csv(file)
		except:
			print("class_ConsumptionFile error : problem when read the file (maybe filedoesn't exist) (add the path with'\\'")
			sys.exit(2)
		self.quality=len(self.df)
		self.init_data_weekday_average()
		self.init_data_month_average()
		# self.save_csv("output\TEST_etape2 après parsing.csv")
		self.passer_en_pas_horaire()
		# self.save_csv("output\TEST_etape3_passage en pas horaire.csv")
		self.missing_periods_detection_V2() #"ne pas compléter l'année")
		# self.missing_time_complete_year_V1()
		# self.missing_periods_detection_V1()
		# self.save_csv("output\TEST_etape3 ajout periodes manquantes.csv")
		
		self.init_coef_mensuels()
		self.missing_data_detection()
		# self.save_csv("output\TEST_etape4 ajout données manquantes.csv")
		self.save_csv("output_formated\\"+self.filename+"_formated.csv",True)
		self.file_formatted = "output_formated\\"+self.filename+"_formated.csv"

	def display(self):
		print("path_file :",self.file)
		print("file :",self.filename)
		# print("data :\n", self.df)
		# print(self.df.head(8))

	def save_csv(self, name='output/TEST.csv',final=TEST_SAUVEGARDER_CSV_INTERMEDIAIRE):
		if final:
			df_temp = self.df.set_index('measurementDate')
			if 'date' in df_temp.columns:
				df_temp = df_temp.drop(['date'], axis=1)
			df_temp.to_csv(name,',')

	def debug(self):
		self.df.to_csv('output/debug_self.df_.csv')

	def graphique(self,mode="affichage"):
		import matplotlib.pyplot as plt
		df_temp=self.df
		for i in range(len(df_temp)):
			df_temp.loc[i,"date"] = fonctions_convert.convert_ElanceFormat_to_date(df_temp.loc[i, "measurementDate"], df_temp.loc[i, "measurementHour"])
		# print(df_temp.dtypes)
		df_temp.plot(x ='date', y='value', kind = 'line')
		plt.xlabel('Time')
		plt.ylabel('W')
		plt.title('Consommation ('+str(self.quality*100/365*24*2)+'%)')
		if mode == "affichage" :
			plt.show()
		else:
			plt.savefig("output_formated/"+self.filename+".png")
		# plt.savefig('graphique.png')

	
	def analyses(self):
		# print(self.df.columns)
		# todo : verifier l'entete
		if self.df.head(0).columns!=['measurementDate', 'measurementHour', 'value']:
			print("error : header not correct")
			sys.exit(2)
		# todo : si date identique ?

	'''
	# ===========================================================================================
	# traitements : estimations
	# ===========================================================================================
	'''
	def init_data_weekday_average(self):
		temp_df_average=self.df.assign(weekday=0)
		for i in range(len(self.df)):
			temp_df_average.loc[i,"weekday"] = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[i, "measurementDate"], self.df.loc[i, "measurementHour"]).isoweekday()
		#tester avec .apply

		# Utilisation d'un Pivot de Table
		self.tcd_weekday_average = temp_df_average.pivot_table(values=["value"], index=["weekday","measurementHour"], aggfunc=np.mean)
		# print(self.tcd)
		# self.tcd.to_csv('output/TCD.csv')

	def get_average_value_for_same_type_of_date_and_same_hour(self,weekday,hour):
		# print(self.tcd.loc[('weekday','1'),("measurementHour","01:00"),"value"])
		if(hour<10):
			hour_str="0"+str(hour)+":00"
		else:
			hour_str=str(hour)+":00"
		return self.tcd_weekday_average.loc[weekday,"value"].loc[hour_str]

	def init_data_month_average(self):
		temp_df_average=self.df.assign(month=0)
		for i in range(len(self.df)):
			temp_df_average.loc[i,"month"] = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[i, "measurementDate"], self.df.loc[i, "measurementHour"]).month

		self.tcd_month_average = temp_df_average.pivot_table(values=["value"], index=["month"], aggfunc=np.min)
		# print(self.tcd_month_average)
		self.tcd_month_average.to_csv('app/output/TCD.csv')

	'''
	# ===========================================================================================
	# traitements : temps
	# ===========================================================================================
	'''

	# fonction qui viendra remplacer missing_time_complete_year et missing_periods_detection en plus rapide !
	def missing_periods_detection_V2(self, option="MODE_COMPLETE_YEAR"):
		start_date_data = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[0, "measurementDate"], self.df.loc[0, "measurementHour"])
		end_date_data = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[len(self.df) - 1, "measurementDate"], self.df.loc[len(self.df) - 1, "measurementHour"])
		if option=="MODE_COMPLETE_YEAR":
			start_date_final = datetime(start_date_data.year, 1, 1,0)
			end_date_final = datetime(end_date_data.year, 12, 31,23)
		else:
			start_date_final = start_date_data
			end_date_final = end_date_data
		pas_horaires = pd.date_range(start_date_final,end_date_final, freq='H')
		dfh = pd.DataFrame({'date': pas_horaires})
		dfh.set_index("date", inplace = True)
		dftemp = self.df
		dftemp.set_index("date", inplace = True)
		dftemp = pd.concat([dfh,dftemp], axis=1)
		dftemp['index'] = range(0, len(dftemp))
		dftemp['date'] = dftemp.index
		dftemp.set_index("index", inplace = True)
		for i in range(len(dftemp)):
			dftemp.loc[i,"measurementDate"]= fonctions_convert.convert_date_to_JJ_MM_AAAA(dftemp.loc[i, "date"])
			dftemp.loc[i,"measurementHour"]= fonctions_convert.convert_date_to_HH_MM(dftemp.loc[i, "date"])
		self.df = dftemp .reindex(columns=['measurementDate','measurementHour','value','date'])

	"""
	def missing_time_complete_year_V1(self):
		# print(self.df.loc[0,"measurementDate"], self.df.loc[0,"measurementHour"])
		# print(self.df.loc[len(self.df)-1,"measurementDate"], self.df.loc[len(self.df)-1,"measurementHour"])
		start_date_data = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[0,"measurementDate"], self.df.loc[0,"measurementHour"]) 
		end_date_data = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[len(self.df)-1,"measurementDate"], self.df.loc[len(self.df)-1,"measurementHour"]) 
		# print(start_date_data,"->",end_date_data)
		start_date_final = datetime(start_date_data.year, 1, 1,0)
		end_date_final = datetime(end_date_data.year, 12, 31,23)
		# print(start_date_final,'->',end_date_final)
		if start_date_final<start_date_data:
			self.df=fonctions_supplementaires_pandas.add_missing_period(self.df,0,start_date_final,start_date_data+timedelta(hours=-1))
		if end_date_final>end_date_data:
			self.df=fonctions_supplementaires_pandas.add_missing_period(self.df,len(self.df),end_date_data+timedelta(hours=1),end_date_final)
	
	def missing_periods_detection_V1(self):
		# print(self.df.head(8))
		flag_premiere_ligne=True
		nb_trous_de_temps=0

		# indexNames = df[ (df['Price'] >= 30)
        #         & (df['Price'] <= 70) ].index
		# df.drop(indexNames , inplace=True)

		# trou de temps ?
		# heure hiver, heure été : négligeable sur un an, on peut s'en passer
		for i in range(len(self.df)):
			if flag_premiere_ligne:
				flag_premiere_ligne=False
			else:
				date_i = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[i,"measurementDate"], self.df.loc[i,"measurementHour"])
				date_precedente = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[i-1,"measurementDate"], self.df.loc[i-1,"measurementHour"])
				tdelta = date_i - date_precedente
				# print(type(tdelta))
				# print(i,date_precedente,"   ",date_i,"    delta:",tdelta)
				if(tdelta==timedelta(minutes=30)):
					print("pas 30 minutes non gérés")
					sys.exit(2)
				if(tdelta==timedelta()):
					print("temps entre deux dates = 0",self.file,"à",date_i)
					print(len(self.df))
					self.df.loc[i].drop()
					print(len(self.df))
					sys.exit(2)
				if(tdelta<timedelta(hours=1)):
					print("temps entre deux dates < 1h delta:",tdelta,self.file,"à",date_i)
					sys.exit(2)
				elif(tdelta>timedelta(hours=1)):
					nb_trous_de_temps+=1
					self.df=fonctions_supplementaires_pandas.add_missing_period(self.df,i,date_precedente+timedelta(hours=1),date_i+timedelta(hours=-1))

		print("nb trous de temps =",nb_trous_de_temps)
		# print(self.df.head(8))
		# print(self.df.tail(0))
		# colonnes=["measurementDate","measurementHour","value"]
		# df = pd.DataFrame(data=c,columns=colonnes)
		# df = df.set_index('measurementDate')
	"""
	def passer_en_pas_horaire(self):
		#ajout colonne type date
		for i in range(len(self.df)):
			self.df.loc[i,"date"]= fonctions_convert.convert_ElanceFormat_to_date_heure_pleine(self.df.loc[i, "measurementDate"], self.df.loc[i, "measurementHour"])
		# Utilisation d'un Pivot de Table
		tcd = self.df.pivot_table(values=["value"], index=["date"], aggfunc=np.mean)
		tcd = tcd.reset_index()
		#ajout colonnes measurementDate measurementHour
		for i in range(len(tcd)):
			tcd.loc[i,"measurementDate"]= fonctions_convert.convert_date_to_JJ_MM_AAAA(tcd.loc[i, "date"])
		for i in range(len(tcd)):
			tcd.loc[i,"measurementHour"]= fonctions_convert.convert_date_to_HH_MM(tcd.loc[i, "date"])
		# ET SI DONNEES MANQUANTES? : no problemo
		self.df = tcd.reindex(columns=['measurementDate','measurementHour','value','date'])


	'''
	# ===========================================================================================
	# traitements : données
	# ===========================================================================================
	'''
	def missing_data_detection(self):
		# print(self.df.head(8))
		flag_premiere_ligne=True

		flag_missing_data=False
		ligne_debut=0
		ligne_fin=0
		nb_trous_de_donnees=0
		# trou de temps ?
		# heure hiver, heure été : négligeable sur un an, on peut s'en passer
		for i in range(len(self.df)):
			# print(self.df.loc[i,"value"])
			if(math.isnan(self.df.loc[i,"value"]) and flag_missing_data==False):
				ligne_debut=i
				flag_missing_data=True
			
			#fin de la période de trou de données
			if((not math.isnan(self.df.loc[i,"value"]) or i==len(self.df)-1) and flag_missing_data==True): 
				flag_missing_data=False
				nb_trous_de_donnees+=1
				# print(i,len(self.df)-1)
				ligne_fin=i-1
				if(i==len(self.df)-1):
					ligne_fin=i
				taille_trou_de_donnees = ligne_fin-ligne_debut +1
				print("trou de données",taille_trou_de_donnees,"de",ligne_debut,"à",ligne_fin)
				# print(self.df.loc[ligne_fin,"measurementDate"], self.df.loc[ligne_fin,"measurementHour"], self.df.loc[ligne_fin,"value"])	
				
				# remplir les données :
				for j in range(ligne_debut,ligne_fin+1):
					# print(j)
					self.df=self.replace_missing_data(self.df,taille_trou_de_donnees,j,ligne_debut,ligne_fin)

		print("nb trous de données =",nb_trous_de_donnees)
		self.df[['value']] =self.df[['value']].astype(int)




	def replace_missing_data(self,df,taille_trou,ligne,ligne_debut,ligne_fin):
		#tester si juste la dernière valeur est manquante
		#arrondir les resulat
		if taille_trou<=6:
			#patch si dernière ligne :
			if ligne_fin+1==len(df):
				estimate_value=df.loc[ligne_debut-1,"value"]
			else:
				#fin patch
				estimate_value=(df.loc[ligne_debut-1,"value"]+df.loc[ligne_fin+1,"value"])/2
			#print(ligne,estimate_value)
			df.loc[ligne,"value"]=int(round(estimate_value))

		elif taille_trou <= 24*30:
			#chercher d'abord une date dans le future car on a potentiellement remplacé le passé
			FLAG=False
			date_ligne = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[ligne, "measurementDate"], self.df.loc[ligne, "measurementHour"])
			#print("objectif:",date_ligne,date_ligne.isoweekday(),date_ligne.hour)
			for c in [1,2,3,4,5,-1,-2,-3,-4,-5]:
				i=ligne+24*7*c
				if i>=len(self.df) or i<=-1:
					#c'est le début ou la fin du fichier, on passe au suivant
					continue
				date_temp = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[i, "measurementDate"], self.df.loc[i, "measurementHour"])
				#print("trouvé:",i,date_temp,date_temp.isoweekday(), date_temp.hour)
				if(date_temp.isoweekday()==date_ligne.isoweekday() and date_temp.hour==date_ligne.hour):
					if not(math.isnan(df.loc[i,"value"])):
						estimate_value=df.loc[i,"value"]
						df.loc[ligne,"value"]=int(round(estimate_value))
						FLAG=True
						break
			
			#si pas de solution ?
			if FLAG==False:
				self.debug()
				print("error estimate data missing < 1 month")
				sys.exit()
		else:
			#méthode1 (linéaire)
			# offset_to_do=0
			# date_ligne =fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[ligne,"measurementDate"], self.df.loc[ligne,"measurementHour"])
			# estimate_value=self.get_average_value_for_same_type_of_date_and_same_hour(date_ligne.isoweekday(),date_ligne.hour) - offset_to_do + offset_to_do
			# df.loc[ligne,"value"]=int(round(estimate_value))
			
			#méthode2 ()
			date_ligne = fonctions_convert.convert_ElanceFormat_to_date(self.df.loc[ligne, "measurementDate"], self.df.loc[ligne, "measurementHour"])
			# print(date_ligne.isoweekday(),date_ligne.hour)
			mois=self.df.loc[ligne,"date"].month
			offset_to_do=self.df_coefs_mensuels.loc[mois,"offset_a_appliquer"]
			estimate_value=self.get_average_value_for_same_type_of_date_and_same_hour(date_ligne.isoweekday(),date_ligne.hour) + offset_to_do
			df.loc[ligne,"value"]=int(round(estimate_value))



		return df
		


	'''
	# ===========================================================================================
	# traitements : données
	# ===========================================================================================
	'''

	def init_coef_mensuels(self):
		# Coef "U shapes" (5 curves )	96,71,70,60,60,58,52,58,52,59,79,91
		# Coef "W shapes" (9 curves )	86,62,57,39,42,63,65,82,44,35,49,93

		coef_mensuel = np.array([86,62,57,39,42,63,65,82,44,35,49,93])
		df_coefs_mensuels = pd.DataFrame(coef_mensuel, index = [1,2,3,4,5,6,7,8,9,10,11,12], columns = ['coef_mensuel'])

		# calculer offset mois présent avec un pivottable min mois
		df=self.df
		# grp = df.groupby(by=[df["date"].map(lambda x : x.hour),
                    #    df["date"].map(lambda x : x.minute)])
		# grp = df.groupby(by=[df['date'].month()])
		# la moyenne des minimum par jour
		grp = df.groupby([df['date'].dt.month,df['date'].dt.day]).min()
		grp = grp.groupby([grp['date'].dt.month]).mean()
		df_coefs_mensuels = pd.concat([df_coefs_mensuels,grp], axis=1)
		df_coefs_mensuels.rename(columns = {'value':'moy des min journalier'}, inplace = True)
		
		# correction offset = moy données réelles = 
		correction_offset = df_coefs_mensuels['moy des min journalier'].mean()
		#todo on peut enlever les jours où on trouve des 0 pour etre plus précis

		# equivalent 100% par mois :
		for i in range(1, len(df_coefs_mensuels)+1):
			df_coefs_mensuels.loc[i,"equivalent_100%_par_mois"] = df_coefs_mensuels.loc[i,"moy des min journalier"]*100/df_coefs_mensuels.loc[i,"coef_mensuel"]
			
		moyenne_equiv_100 = df_coefs_mensuels["equivalent_100%_par_mois"].mean()

		for i in range(1, len(df_coefs_mensuels)+1):
			df_coefs_mensuels.loc[i,"offset_a_appliquer"] =-correction_offset + moyenne_equiv_100*(df_coefs_mensuels.loc[i,"coef_mensuel"]/100)
		
		"""print("paramètres d'estimation méthode 2")
		print('correction_offset :',correction_offset)
		print('moyenne_equiv_100 :',moyenne_equiv_100)
		print(df_coefs_mensuels)"""
		# print(df_coefs_mensuels)
		self.df_coefs_mensuels = df_coefs_mensuels



	def init_lissage_courbe_par_semaine():
		a=np.linspace(1,52,52)
		b=[1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,11,12,12,12,12,12]
		df_coefs_hebdo = pd.DataFrame(b, index = a, columns = ['mois_ref'])
		print(df_coefs_hebdo)

		# df_coefs_mensuels["moy_mobile"]=df_coefs_mensuels["offset_mensuel"].rolling(2).mean()


	# init_lissage_courbe_par_semaine()