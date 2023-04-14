import json

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
						arquivo.write(verso["texto"])


