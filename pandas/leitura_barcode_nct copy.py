import os
import pandas as pd
from pdf2image import convert_from_path
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
from flask import Blueprint, render_template, request
from pathlib import Path


    
caminhoPasta = Path("U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE")
planNCT = pd.read_excel("static\\data\\arquivo-nao-contribuinte\\Não Contribuintes.xlsx")
pastapng = r"static\data\gnre"

linha = 0

NFE = "103048"

# Montando o caminho
caminhoPastaGNRE = r'U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE 2025\09. ARQUIVO GNRE SET 2025'

if os.path.exists(caminhoPastaGNRE):

    pdfs = [i for i in os.listdir(caminhoPastaGNRE) if ".pdf" in i]
    print(pdfs)

    pages = convert_from_path(caminhoPastaGNRE+"\\"+ NFE +" ST.pdf", dpi=500, poppler_path=r'poppler-24.08.0\Library\bin')
    print(caminhoPastaGNRE + "\\" + NFE + " DAR.pdf")

    savegnre = pastapng + "\\" + NFE

    for page in pages:
        page.save(savegnre+".png", 'PNG')

    frame = cv2.imread(savegnre+".png")
    detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])
    # print(ZBarSymbol.type)

    if not detectedBarcode:
        print("Código de barras nao lida")

    else:
        for barcode in detectedBarcode:
            if barcode.data != "":
                print(barcode.data.decode("UTF-8"))


    # def deletando_arquivos(folder_path):

    #     try:
    #         files = os.listdir(folder_path)
    #         if len(files) == 0:
    #             print(f"Sem arquivos a deletar")
    #         else:
    #             for file in files:
    #                 file_path = os.path.join(folder_path, file)
    #                 if os.path.isfile(file_path):
    #                     os.remove(file_path)
    #                 print("Feito!")
    #     except OSError:
    #         print("Erro, verificar")


    # deletando_arquivos(pastapng)
        


