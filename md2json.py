"""
with open("lde-single-file.md") as file:
	for line in file:
		if not line:
			continue # pula linhas vazias
		if line[0] in ["#"]: # capitulo
		if line[0] in ["0"]: # pergunta
		if line[0] in [">"]: # resposta
		# nota

/lde.0.3.01/ Introdução 01
livro = [parte]
parte = [capitulo]
capitulo = [itens]
item = [versos]
verso = (nota | pergunta | resposta)

livro = [[[[[{notas}]]]]]

livro = {id, cod, nome, partes}
parte = {id, cod, nome, capitulos}
capitulo = {id, cod, nome, itens}
item = {id, cod, nome, versos}
verso = {id, cod, tipo, texto}

id = "lde" | 0..99
cod = "lde.0.3.01"
verso.tipo = nota | pergunta | resposta
"""
import json

def verificar_tipo(linha, parte):
	if 1 <= parte <= 4:
		"""if linha[0].isnumeric():
			return "pergunta"
		if linha[0] == "[" and linha[1].isnumeric():
			return "pergunta" """
		if linha[0] == "`" and linha[6].isnumeric():
			return "pergunta"
	if linha[0] == ">":
		return "resposta"
	return "nota"

def gerar_codigo(linha, tipo):
	if tipo != "pergunta":
		return 0
	if linha[0] == "`":
		return linha.split("`")[1]
	livro = "lde"
	tokens = linha.split(" ")
	pergunta = tokens[0][:-1]
	letra = tokens[1][:-1] if tokens[1][-1] == ")" else ""
	cod = livro + ".q" + pergunta + letra
	return cod

def filtrar(linha):
	if not linha:
		return linha
	linha = remove_hl(linha)
	linha = remove_nl(linha)
	return linha

def remove_hl(linha):
	# verifica se pergunta tem hyperlink e o remove
	if linha[0] == "[" and linha[1].isnumeric():
		numero = linha.split("]")[0][1:]
		texto = " ".join(linha.split(" ")[1:])
		if len(numero.split(".")) > 1:
			return numero.split(".")[0] + ". " + numero.split(".")[1] + ") " + texto
		return numero + ". " + texto
	return linha

def remove_nl(line):
	return line[:-1] if line[-1:] == "\n" else line

livros = []
with open("1lde-single-file.md", encoding="utf8") as arquivo:
	livro = parte = capitulo = item = verso = -1
	for linha in arquivo:
		if not linha or linha == "\n":
			continue # pula linhas vazias
		if linha[0] == "#": # capitulo
			hashtags = linha.split(" ")
			importancia = len(hashtags[0])
			cod = hashtags[1][1:-1] if hashtags[1][1:4] == "lde" else hashtags[2][1:-1]
			nome = filtrar(" ".join(hashtags[3:]))
			obj = {'cod': cod, 'nome': nome}
			if importancia == 1: # livro
				livro += 1
				parte = capitulo = item = verso = -1
				obj.update({'id': livro, 'partes': []})
				livros.append(obj)
			elif importancia == 2: # parte
				parte += 1
				capitulo = item = verso = -1
				obj.update({'id': parte, 'capitulos': []})
				livros[livro]["partes"].append(obj)
			elif importancia == 3: # capitulo
				capitulo += 1
				item = verso = -1
				obj.update({'id': capitulo, 'itens': []})
				livros[livro]["partes"][parte]["capitulos"].append(obj)
			elif importancia == 4: # item
				item += 1
				verso = -1
				obj.update({'id': item, 'versos': []})
				livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"].append(obj)
			elif importancia == 5: # indice geral
				verso += 1
				tipo = verificar_tipo(linha, parte)
				cod = gerar_codigo(linha, tipo)
				obj = {'id': verso, 'cod': cod, 'tipo': tipo, 'texto': filtrar(linha)}
				livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"][item]["versos"].append(obj)
			continue
		# versos
		if item == -1:
			item += 1
			verso = -1
			tipo = verificar_tipo(linha, parte)
			cod = gerar_codigo(linha, tipo)
			obj = {'id': item, 'cod': cod, 'nome': "", 'versos': []}
			livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"].append(obj)
		verso += 1
		tipo = verificar_tipo(linha, parte)
		cod = gerar_codigo(linha, tipo)
		obj = {'id': verso, 'cod': cod, 'tipo': tipo, 'texto': filtrar(linha)}
		#print(livro, parte, capitulo, item, verso, linha)
		#print(livros)
		livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"][item]["versos"].append(obj)

#print(json.dumps(livros))
with open("livros.json", "w", encoding='utf8') as arquivo:
	json.dump(livros, arquivo, indent=4, ensure_ascii=False)

livros = []



