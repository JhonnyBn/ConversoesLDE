import json
import re

def filtro(verso, parte, capitulo):
	if parte["id"] > 5 and capitulo["id"] == 1:
		if len(verso["texto"]) > 5:
			q = re.split('(\d+)', verso["texto"])
			if len(q) > 1 and q[-2].isnumeric():
				numero = q[-2]
				letra = q[-1][:-2]
				return " ".join(verso["texto"].split(" ")[:-1]) + " [lde.q" + numero + letra + "](#lde.q" + numero + letra + ")\n"
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

with open("livros.json", encoding='utf-8') as arquivo:
	livros = json.load(arquivo)

#print(livros)

with open("output.md", "w", encoding='utf-8') as arquivo:
	for livro in livros:
		arquivo.write("# 📔 /" + livro["cod"] + "/ " + livro["nome"])
		for parte in livro["partes"]:
			arquivo.write("## 🗂️ /" + parte["cod"] + "/ " + parte["nome"])
			for capitulo in parte["capitulos"]:
				arquivo.write("### 📑 /" + capitulo["cod"] + "/ " + capitulo["nome"])
				for item in capitulo["itens"]:
					if item["nome"]:
						arquivo.write("#### 📃 /" + item["cod"] + "/ " + item["nome"])
					for verso in item["versos"]:
						arquivo.write(filtro(verso, parte, capitulo))


