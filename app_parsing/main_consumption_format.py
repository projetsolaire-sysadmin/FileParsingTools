import class_ConsumptionFile


def main():
	
	# p = class_ConsumptionFile.class_ConsumptionFile(inputfile)
	# #p.display()
	# p.analyses()
	# p.data_missing_complete_year()
	# p.save_csv('output/TEST_completer_annee_1.csv')
	# p.data_missing_periods()
	# p.save_csv('output/TEST_completer_annee_2.csv')

	q = class_ConsumptionFile.class_ConsumptionFile('output/TEST_completer_annee_1.csv')
	#q.graphique()


def test_de_A_a_Z():
	inputfile ="data\Enedis_SGE_HDM_A07F1HSA.csv"
	# parser le fichier
	q = class_ConsumptionFile.class_ConsumptionFile(inputfile)

if __name__ == "__main__":
	main()
