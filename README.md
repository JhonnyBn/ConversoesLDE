# ConversoesLDE
Convertendo o Livro dos Espíritos em txt, md, json, etc.

Convertendo o livro .md para um formato programático com mais informações (JSON):
Input: lde-single-file.md
Uso: Abra o terminal e execute: `python md2json.py`
Output: livros.json

Convertendo o JSON para qualquer formato (inicialmente de volta pra MD):
Input: livros.json
Uso: Abra o terminal e execute: `python json2md.py`
Output: output.md

Observação: o programa usa python na versão 3, em caso de linux pode ser necessário executar o comando `python3`