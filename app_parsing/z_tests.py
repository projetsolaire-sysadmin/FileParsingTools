

"""
ligne_debut=133
ligne_fin=135

for i in range(ligne_debut-1,ligne_debut-24*7,-1):
	print(i)				

for i in range(ligne_fin+1,ligne_fin+24*7,1):
	print(i)
"""

str = "./upload_files/Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv"
str = ".\\upload_files\\Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv"

# str = "Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv"
def _test_str():
	for str in ["./upload_files/Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv",
				".\\upload_files\\Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv",
				"Fonderies du midi - Enedis_SGE_HDM_A079I4LV.csv"]:
		if '\\' in str:  
			temp=str.split('\\')
			res= temp[len(temp)-1]
		elif '/' in str:
			temp=str.split('/')
			res= temp[len(temp)-1]
		else:
			res=str
		print(res)

_test_str()