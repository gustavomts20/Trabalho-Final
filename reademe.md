# Introdução

Este Código em Python implementa um analisador léxico, sintático e semântico usando
a biblioteca PLY (Python Lex-Yacc). Serve para analisar e executar uma série de operações baseadas na linguagem C,
que incluem declarações de variáveis, atribuições, e estruturas de controle como laços e condicionais.

Para executar o código, é necessário instalar a biblioteca PLY para Python.

`pip install ply`

# Arquivos Necessários

- `input.txt`: O arquivo deve conter o código em C que se deseja compilar.

# Execução

python compilador.py

# Estrutura do Código

- **Definições Léxicas**: O código começa definindo os tokens necessários para a análise léxica, incluindo operadores, tipos de dados e palavras reservadas.

- **Analisador Léxico**: Usa expressões regulares para identificar os tokens no texto de entrada, os quais serão utilizados nas próximas etapas da análise.

- **Analisador Sintático**: Define uma série de regras gramaticais que descrevem a sintaxe da linguagem e como as entradas devem ser processadas e analisadas. Este analisador constrói uma árvore sintática baseada na entrada de tokens gerados pelo analisador léxico.

- **Análise Semântica**: O script verifica se as variáveis foram declaradas antes de seu uso, se as operações são realizadas entre tipos compatíveis e se as variáveis não são redeclaradas no mesmo escopo. Erros semânticos são reportados durante a execução das regras gramaticais.

# Logs de análise

Foi utilizado o módulo `logging` para criar logs detalhados do processo de análise, que são salvos no arquivo `parselog.txt`. Eles incluem informações de todas as fases da análise, ajudando no entendimento do fluxo de processamento.

parselog.txt: Arquivo de log onde os detalhes do processo de análise serão gravados.
