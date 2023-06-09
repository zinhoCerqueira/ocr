#!/usr/bin/env python3
from flask import Flask, request, jsonify
import re
import requests
import os

from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
from PIL import Image

'''
Exemplos

link q recebe = 'https://drive.google.com/file/d/ID_DO_ARQUIVO/view'
link q monta = 'https://drive.google.com/u/0/uc?id=ID_DO_ARQUIVO&export=download'
'''

app = Flask(__name__)

def download_pdf_file(url: str, filename: str) -> str:
    """Download PDF from given URL to local directory.

    :param url: The URL of the PDF file to be downloaded
    :return: The name of the downloaded PDF file if successful, otherwise an empty string.
    """
    # Request URL and get response object
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Save in the current working directory
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{filename} foi salvo!')
            return start_analise(url)
    else:
        print(f'Não foi possível realizar o download do pdf: {url}')
        print(f'HTTP response status code: {response.status_code}')
        return ""

def start_analise(url):
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\OCR\Tesseract.exe'

    arquivo = "pdf.pdf"

    data = convert_pdf_img(arquivo)

    texto_completo = analise_texto(arquivo)

    valor_reitor = False

    for i, img in enumerate(data):
        # Convertendo a imagem em formato OpenCV
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Aplicando OCR na imagem
        custom_config = r'--oem 3 --psm 6'
        result = pytesseract.image_to_string(img_cv, config=custom_config)

        # Exibindo o resultado
        # print("Texto na página", i+1, "do PDF:")
        # print(result)
        # print("============================")

        # Caso seja a primeira página do documento, pegue o número da resolução e o ano correspondente.
        if i == 0:
            resol, ano, data, cabecalho = analise_pagina_1(result)
        
        # Analisa em alguma página se encontra o formato especifico onde se nomeia o reitor/reitora.
        if not valor_reitor:
            reitor = analise_reitora(result)
            if reitor != "####":
                valor_reitor = True

    print("Resolução: ", resol)
    print("Ano: ", ano)
    print("Data: ", data)
    print("Cabeçalho: ", cabecalho)
    print("Reitor: ", reitor)
    print("Texto Completo: ", texto_completo)

    data = {
        "numero":resol,
        "ano":ano,
        "data":data,
        "reitor":reitor,
        "cabecalho":cabecalho,
        "texto":texto_completo,
        "link":url
    }

    return jsonify(data)

# Converte o pdf em imagens, o tesseract apenas trabalha com imagens.
def convert_pdf_img(pdf):

    # Caminho para o arquivo PDF
    pdf_path = pdf

    # Convertendo a primeira página do PDF em imagem
    images = convert_from_path(
    pdf_path, 500, poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')

    return images

def analise_pagina_1(texto):

    padrao_resolucao = r"[Rr][Ee][Ss][Oo][Ll][Uu][ÇCGcçg][Aa][Oo]\s(CONSEPE|CONSU)\s(\d+\s/\s(\d+))"
    padrao_data = r"(?<!\d)\d{1,2}\s?/\s?\d{1,2}\s?/\s?\d{4}(?!\d)"
    padrao_cabecalho = r"\b(\d{1,2}\s?/\s?\d{1,2}\s?/\s?\d{4})\b\s(.*?)RESOLVE:"



    resultado = re.search(padrao_resolucao, texto)
    resultado_data = re.search(padrao_data, texto)
    resultado_cabecalho = re.search(padrao_cabecalho, texto, re.DOTALL)
    
    # Pega os dados referentes a resolução
    if resultado:
        n_Resolucao = resultado.group(2)
        ano = resultado.group(3)

    # Caso a resolução não seja encontrada retorna uma string com 4#
    else:
        n_Resolucao = ano = "####"

    # Pega os dados referentes a data
    if resultado_data:
        data = resultado_data.group()
    else:
        data = "####"
    
    # Pega os addos referentes ao cabeçalho
    if resultado_cabecalho:
        cabecalho = resultado_cabecalho.group(2)
    else:
        cabecalho = "####"
        
    return n_Resolucao, ano, data, cabecalho

def analise_reitora(texto):
    padrao_reitor = r"Documento assinado eletronicamente por\s(.*?)(?=,)"
    valor_encontrado = re.search(padrao_reitor, texto)

    if valor_encontrado:
        valor = valor_encontrado.group(1)
    else:
        valor = "####"

    return valor

def analise_texto(pdf):

    imagens = convert_pdf_img(pdf)
    largura, altura = imagens[0].size
    imagem_final = Image.new("RGB", (largura, altura*len(imagens)))
    count = 0

    for i in imagens:

        imagem_final.paste(i, (0, altura*count))
        count = count + 1

    img_cv = cv2.cvtColor(np.array(imagem_final), cv2.COLOR_RGB2BGR)

    # Aplicando OCR na imagem
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(img_cv, config=custom_config)

    # Aplicando o regex
    padrao = r"RESOLVE:(.*?)Documento assinado eletronicamente por"
    correspondencia = re.search(padrao, result, re.DOTALL)

    if correspondencia:
        texto_capturado = correspondencia.group(1)

    else:
        print("Nenhuma correspondência encontrada.")

    return texto_capturado


@app.route('/download-pdf', methods=['GET'])
def handle_download_pdf():
    url = request.args.get('url')

    if url:
        match = re.search(r"/d/([^/]+)/", url)
        if match:
            id = match.group(1)
            urlDownload = f'https://drive.google.com/u/0/uc?id={id}&export=download'
            file_path = 'pdf.pdf'
            filename = download_pdf_file(urlDownload, file_path)

            if filename:
                return filename
            else:
                return f'Não foi possível realizar o download do pdf: {urlDownload}'
    else:
        return 'Não foi possível processar.'

if __name__ == '__main__':
    app.run()