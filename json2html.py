import json

def filtro(verso, parte, capitulo):
	if verso["tipo"] == "pergunta":
		if verso["texto"][0] != "`":
			return "`" + verso["cod"] + "` " + verso["texto"]
	return verso["texto"]

def html_livro(verso, parte):
	if parte == "pre":
		return "<div>"
	elif parte == "titulo":
		return "<div>" + verso + "</div>"
	elif parte == "pos":
		return "</div>"
	return ""

def codigo(importancia, secao, conteudo):
	if importancia == "livro":
		return html_livro(conteudo, secao)
	elif importancia == "":
		return html_()
	return a

with open("livros.json", encoding='utf-8') as arquivo:
	livros = json.load(arquivo)

#print(livros)

anterior = ""
nl = "\n\n"
with open("output.html", "w", encoding='utf-8') as arquivo:
	for livro in livros:
		arquivo.write("# `" + livro["cod"] + "` 📔 " + livro["nome"] + nl)
		for parte in livro["partes"]:
			arquivo.write("## `" + parte["cod"] + "` 🗂️ " + parte["nome"] + nl)
			for capitulo in parte["capitulos"]:
				arquivo.write("### `" + capitulo["cod"] + "` 📑 " + capitulo["nome"] + nl)
				for item in capitulo["itens"]:
					if item["nome"]:
						arquivo.write("#### `" + item["cod"] + "` 📃 " + item["nome"] + nl)
					for verso in item["versos"]:
						if verso["tipo"] == "resposta":
							arquivo.write(filtro(verso, parte, capitulo) + "\n")
						elif anterior == "resposta":
							arquivo.write("\n" + filtro(verso, parte, capitulo) + nl)
						else:
							arquivo.write(filtro(verso, parte, capitulo) + nl)
						anterior = verso["tipo"]


