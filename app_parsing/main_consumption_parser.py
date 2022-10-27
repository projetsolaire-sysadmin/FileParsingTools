import class_EnedisSGEFormatParser

def main():
	inputfile ="data\Enedis_SGE_HDM_A07F1HSA.csv"
	p = class_EnedisSGEFormatParser.class_EnedisSGEFormatParser(inputfile)
	p.afficher()
	p.parse()

if __name__ == "__main__":
	main()

