from pdf2image import convert_from_path
import re
import cv2
import openai
import numpy as np
import pytesseract

# Prepara uma lista de dados previamente verificados de resoluções
# aleatórias do CONSEPE. Ela será comparada com os dados obtidos pelo
# OCE e verificar a taxa de acerto desta analise.

def aleatory_resolution():

    resolutions = [
        {
            "numero": "01/82",
            "ano": 1982,
            "data": "09/12/1982",
            "reitor": "José Maria Nunes Marques",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "02/82",
            "ano": 1982,
            "data": "09/12/1982",
            "reitor": "José Maria Nunes Marques",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "01/98",
            "ano": 1998,
            "data": "29/01/1998",
            "reitor": "José Onofre Gurjão Boavista da Cunha",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "01/2000",
            "ano": 2000,
            "data": "05/01/2000",
            "reitor": "Anaci Bispo Paim",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "001/2005",
            "ano": 2005,
            "data": "03/01/2005",
            "reitor": "José Onofre Gurjão Boavista da Cunha",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "001/2008",
            "ano": 2008,
            "data": "17/01/2008",
            "reitor": "Washington Almeida Moura",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "001/2010",
            "ano": 2010,
            "data": "12/01/2010",
            "reitor": "José Carlos Barreto de Santana",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "01/2014",
            "ano": 2014,
            "data": "23/01/2014",
            "reitor": "José Carlos Barreto de Santana",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "001/2018",
            "ano": 2018,
            "data": "19/01/2018",
            "reitor": "Evandro do Nascimento Silva",
            "cabecalho": "",
            "texto": "",
            "link": ""
        },
        {
            "numero": "059/2023",
            "ano": 2023,
            "data": "19/05/2023",
            "reitor": "Amali de Angelis Mussi",
            "cabecalho": "",
            "texto": "",
            "link": ""
        }

    ]
    print("Resoluções de Teste")

# Converte o pdf em imagens, o tesseract apenas trabalha com imagens.
def convert_pdf_img():

    # Caminho para o arquivo PDF
    pdf_path = "pdfs/p10.pdf"

    # Convertendo a primeira página do PDF em imagem
    images = convert_from_path(
    pdf_path, 500, poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')

    return images

def analise_Resolucao(texto):

    padrao_resolucao = r"[Rr][Ee][Ss][Oo][Ll][Uu][ÇCGcçg][Aa][Oo]\s(CONSEPE|CONSU)\s(\d+\s/\s(\d+))"
    padrao_data = r"(?<!\d)\d{1,2}\s?/\s?\d{1,2}\s?/\s?\d{4}(?!\d)"


    resultado = re.search(padrao_resolucao, texto)
    resultado_data = re.search(padrao_data, texto)
    
    if resultado:
        n_Resolucao = resultado.group(2)
        ano = resultado.group(3)
        print("Número da Resolução:", n_Resolucao)
        print("Ano:", ano)
    # Caso a resolução não seja encontrada retorna uma string com 4#
    else:
        print("Trecho não encontrado")
        n_Resolucao = ano = "####"

    if resultado_data:
        data = resultado_data.group()
        print("Data:", data)
    else:
        data = "####"
        
    return n_Resolucao, ano, data



# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------
# START -----------------------------------------------------------------------

# aleatory_resolution()

data = convert_pdf_img()
    
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
        print("Analisando a página", i+1)
        resol, ano, data = analise_Resolucao(result)
