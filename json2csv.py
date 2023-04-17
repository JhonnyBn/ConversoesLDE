import json
import csv

def filtro(verso):
	if verso["tipo"] == "pergunta":
		codlivro = "lde"
		texto = verso["texto"]
		temp = texto.split(" ")
		numero = temp[0][:-1]
		subitem = ""
		try:
			if temp[1][-1] == ")":
				subitem = temp[1][:-1]
				texto = " ".join(temp[2:])
			else:
				texto = " ".join(temp[1:])
		except IndexError as e:
			texto = " ".join(temp[1:])
		#[30](#lde.q30).
		#[33.a](#lde.q33a)
		if subitem:
			return "[" + numero + "." + subitem + "](#" + codlivro + ".q" + numero + subitem + "). " + texto
		else:
			return "[" + numero + "](#" + codlivro + ".q" + numero + "). " + texto
	return verso["texto"]

def save_csv(data):
	fname = 'output.csv'
	header = ["Livro", "Parte", "Capítulo", "Item", "Subitem", "Index", "Tipo", "Texto"]
	with open(fname, 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(data)
	return

with open("livros.json", encoding='utf-8') as arquivo:
	livros = json.load(arquivo)

#print(livros)
data = []
with open("output.md", "w", encoding='utf-8') as arquivo:
	for livro in livros:
		for parte in livro["partes"]:
			for capitulo in parte["capitulos"]:
				for item in capitulo["itens"]:
					for verso in item["versos"]:
						if verso["texto"] != "\n":
							data.append([livro["id"], parte["id"], capitulo["id"], item["id"], verso["id"], item["cod"], verso["tipo"], verso["texto"]])

save_csv(data)

