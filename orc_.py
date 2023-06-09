from pdf2image import convert_from_path
import re
import cv2
import openai
import numpy as np
import pytesseract

# Prepara uma lista de dados previamente verificados de resoluções
# aleatórias do CONSEPE. Ela será comparada com os dados obtidos pelo
# OCE e verificar a taxa de acerto desta analise.

# Converte o pdf em imagens, o tesseract apenas trabalha com imagens.
def convert_pdf_img():

    # Caminho para o arquivo PDF
    pdf_path = "pdfs/11.pdf"

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
        print(resultado_cabecalho)
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



# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------

data = convert_pdf_img()
valor_reitor = False
    
# Erro em que o tesseract não é encontrado pelo py
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\OCR\Tesseract.exe'

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
        print(result)
    
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

    

