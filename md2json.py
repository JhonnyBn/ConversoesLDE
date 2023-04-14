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

def verificar_tipo(linha):
	if linha[0].isnumeric():
		return "pergunta"
	if linha[0] == ">":
		return "resposta"
	return "nota"

def gerar_codigo(linha):
	return 0

livros = []
with open("lde-single-file.md", encoding="utf8") as arquivo:
	livro = parte = capitulo = item = verso = -1
	for linha in arquivo:
		if not linha:
			continue # pula linhas vazias
		if linha[0] in ["#"]: # capitulo
			importancia = len(linha.split(" ")[0])
			cod = linha.split(" ")[2][1:-1]
			nome = " ".join(linha.split(" ")[3:])
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
				tipo = verificar_tipo(linha)
				cod = gerar_codigo(linha)
				obj = {'id': verso, 'cod': cod, 'tipo': tipo, 'texto': linha}
				livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"][item]["versos"].append(obj)
			continue
		# versos
		if item == -1:
			item += 1
			verso = -1
			obj = {'id': item, 'cod': gerar_codigo(linha), 'nome': "", 'versos': []}
			livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"].append(obj)
		verso += 1
		tipo = verificar_tipo(linha)
		cod = gerar_codigo(linha)
		obj = {'id': verso, 'cod': cod, 'tipo': tipo, 'texto': linha}
		#print(livro, parte, capitulo, item, verso, linha)
		#print(livros)
		livros[livro]["partes"][parte]["capitulos"][capitulo]["itens"][item]["versos"].append(obj)

#print(json.dumps(livros))
with open("livros.json", "w", encoding='utf8') as arquivo:
	json.dump(livros, arquivo, indent=4, ensure_ascii=False)

livros = []


