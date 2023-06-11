# OCR / Examinador PDF

## Sobre
Este repositório guarda um módulo de um projeto maior responsável por melhorar o acesso a um conjunto de documentos da Universidade Estadual de Feira de Santana.
Este módulo tem a responsabilidade de analisar um arquivo PDF e retornar dados contidos nele, sendo eles : o númerro da resolução, ano, data, reitor, cabeçalho, texto e o link.

## EXA844 e o projeto de extensão
EXA844 é uma disciplina optativa do curso de Engenharia de Computação  da UEFS ministrada por [João Rocha](https://github.com/joaorochajr) com o objetivo de introduzir conceitos de Programação para Redes como sistemas distribuidos, fluxo de dados, programaçao front e back-end e outros frameworks direcionados a programaçao web. Para finalizar a disciplina este desafio requer o desenvolvimento de um engenho de busca para resoluções da UEFS e a parte atribuida a nós ([Gabriel Carvalho](https://github.com/GabCarvaS), [Jader Cerqueira](https://github.com/zinhoCerqueira)) é um código que faça a analise de um PDF e retorne alguns dados.

## O funcionamento do código
Foi escolhido python para o desenvolvimento de toda essa seção já que ela facilita muito o desenvolvimento pelas bibliotecas que agilizariam nossa resulução. Para subir uma API rapidamente usamos o flask por ser um framework leve e fácil de usar para o desenvolvimento web nos fornecendo um vonjunto básico de ferramentas para lidar com solicitações HTTP. Já a extração de dados é feita em partes, a primeira é a conversão dos arquivos pdfs em imagens, já que o tesseract (os verdadeiros olhos do sistema) exige para que sejam feitas as leituras a partir de imagens e não de arquivos pdfs, essa conversão é feita pelo [pdf2img](https://pypi.org/project/pdf2image/). Após esta seção entra em ação o [tesseract](https://pypi.org/project/pytesseract/), que é uma biblioteca de reconhecimento óptico de caractereres (OCR) e já é muito difundido para processar e extrair textos de imagens.


Lembrando que este seção faz parte de um problema maior e também depende de outras partes como esta também depende delas.

## Pontos necessários para instalação correta.

Fica necessário para rodar o projeto corretamente a instalação do poopler para fazer a conversão, a biblioteca do python pede
para ter o funcionamento correto.

Também é necessário fazer a instalação manual do tesseract, caso o pip não "instale corretamente".
