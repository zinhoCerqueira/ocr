from pdf2image import convert_from_path
import re
import cv2
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

def apply_tesseract():

    # Caminho para o arquivo PDF
    pdf_path = "pdfs/p10.pdf"

    # Convertendo a primeira página do PDF em imagem
    images = convert_from_path(
    pdf_path, 500, poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')

    return images

# START -----------------------------------------------------------------------

aleatory_resolution()

data = apply_tesseract()

# Erro em que o tesseract não é encontrado pelo py
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\OCR\Tesseract.exe'

for i, img in enumerate(data):
    # Convertendo a imagem em formato OpenCV
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Aplicando OCR na imagem
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(img_cv, config=custom_config)

    # Procura a Resolução e ano ------------------------------------------------
    if(i == 0):
        
        texto1 = "RESOLUÇÃO CONSEPE Nº 001/2008"
        texto2 = "RESOLUÇÃO CONSEPE 001 / 2008"
        texto3 = "RESOLUÇÃO CONSEPE - 02/82"

        expressao_regular = r"Resolução\sConsepe\s(?:Nº\s)?(\d+/\d+|\d+)"
        # \s: espaço em branco
        # (?:Nº\s)?: corresponde a "Nº " de forma opcional, o ?: é utilizado para criar um grupo não capturador
        # (\d+/\d+|\d+): corresponde a um padrão de número/ano ou apenas número

        resolucao = re.search(expressao_regular, result)
        if resolucao:
            resolucao = resolucao.group(1)
            print("Resolução :", resolucao)
        else:
            print("deu ruim na resolucao")



    # Exibindo o resultado
    print("Texto na página", i+1, "do PDF:")
    print(result)
    print("============================")

