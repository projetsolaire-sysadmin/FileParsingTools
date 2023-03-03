"""import numpy as np
import pandas as pd
import fonctions_convert
from datetime import datetime, timedelta"""

def inserer_ligne_dans_dataframe(ligne,df,valeur):
	# https://fr.acervolima.com/inserer-une-ligne-a-une-position-donnee-dans-pandas-dataframe/
	# 2 méthodes :

	# Méthode 1:
	return Insert_row_1(ligne, df, valeur)

	# Méthode 2:
	# return Insert_row_2(ligne, df, valeur)

# Function to insert row in the dataframe
def Insert_row_1(row_number, df, row_value):
    # Starting value of upper half
    start_upper = 0
  
    # End value of upper half
    end_upper = row_number
  
    # Start value of lower half
    start_lower = row_number
  
    # End value of lower half
    end_lower = df.shape[0]
  
    # Create a list of upper_half index
    upper_half = [*range(start_upper, end_upper, 1)]
  
    # Create a list of lower_half index
    lower_half = [*range(start_lower, end_lower, 1)]
  
    # Increment the value of lower half by 1
    lower_half = [x.__add__(1) for x in lower_half]
  
    # Combine the two lists
    index_ = upper_half + lower_half
  
    # Update the index of the dataframe
    df.index = index_
  
    # Insert a row at the end
    df.loc[row_number] = row_value
   
    # Sort the index labels
    df = df.sort_index()
  
    # return the dataframe
    return df


# Let's create a row which we want to insert
def test_Insert_row_1():
	row_number = 2
	row_value = ['11/2/2011', 'Wrestling', 12000]
	
	if row_number > df.index.max()+1:
		print("Invalid row_number")
	else:
		
		# Let's call the function and insert the row
		# at the second position
		df = Insert_row_1(row_number, df, row_value)
	
		# Print the updated dataframe
		print(df)


# Function to insert row in the dataframe
def Insert_row_2(row_number, df, row_value):
	# Slice the upper half of the dataframe
	df1 = df[0:row_number]

	# Store the result of lower half of the dataframe
	df2 = df[row_number:]

	# Insert the row in the upper half dataframe
	df1.loc[row_number]=row_value

	# Concat the two dataframes
	df_result = pd.concat([df1, df2])

	# Reassign the index labels
	df_result.index = [*range(df_result.shape[0])]

	# Return the updated dataframe
	return df_result

def test_Insert_row_2():
	# Let's create a row which we want to insert
	row_number = 2
	row_value = ['11/2/2011', 'Wrestling', 12000]
	
	if row_number > df.index.max()+1:
		print("Invalid row_number")
	else:
	
		# Let's call the function and insert the row
		# at the second position
		df = Insert_row_2(2, df, row_value)
	
		# Print the updated dataframe
		print(df)

# add missing period :
def add_missing_period(df,i,date1,date2):
	tdelta = date2-date1
	nb_heures = tdelta.total_seconds()//3600
	nb_heures=int(nb_heures)+1
	# print("ajouter",nb_heures,"lignes de",date1,"à",date2)
	for j in range(nb_heures):
		d=date1 + timedelta(hours=j)
		# self.df=self.df.append({'measurementDate' : fonctions_convert.convert_date_to_JJ_MM_AAAA(d) , 'measurementHour' : fonctions_convert.convert_date_to_HH_MM(d) , } , ignore_index=True)
		df=inserer_ligne_dans_dataframe(i+j,df,{'measurementDate' : fonctions_convert.convert_date_to_JJ_MM_AAAA(d) , 'measurementHour' : fonctions_convert.convert_date_to_HH_MM(d) , })
	return df