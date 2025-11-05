import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import date, datetime
import pyautogui as pa
import time
import pyperclip
import xml.etree.ElementTree as ET
import pandas as pd
import cv2 
from pyzbar.pyzbar import decode, ZBarSymbol
from pdf2image import convert_from_path

caminhoPasta = r"U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE 2025\08. ARQUIVO GNRE AGO 2025"
planNCT = pd.read_excel("static\\data\\arquivo-nao-contribuinte\\Não Contribuintes.xlsx")
pastapng = r"static\data\gnre"

linha = 0


for unidadeFederativa in planNCT['UF']:

    if unidadeFederativa == "AL":

        pdfs = [i for i in os.listdir(caminhoPasta) if ".pdf" in i]
        print(pdfs)

        pages = convert_from_path(caminhoPasta+"\\"+str(planNCT.loc[linha, 'NFE'])+".pdf", dpi=500, poppler_path=r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\poppler-24.08.0\Library\bin')
        print(caminhoPasta + "\\" + str(planNCT.loc[linha, 'NFE']) + ".pdf")

        savegnre = pastapng + "\\" + str(planNCT.loc[linha, 'NFE'])

        for page in pages:
            page.save(savegnre+".png", 'PNG')

        frame = cv2.imread(savegnre+".png")
        detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

        if not detectedBarcode:
            print("Código de barras nao lida")
            linhaSpecif = planNCT.index == linha
            planNCT.loc[linhaSpecif, ["Cód Barra"]] = "Código de barras nao lida"

        else:
            for barcode in detectedBarcode:
                if barcode.data != "":
                    print(barcode.data.decode("UTF-8"))
                    linhaSpecif = planNCT.index == linha
                    planNCT.loc[linhaSpecif, ["Cód Barra"]] = [barcode.data.decode("UTF-8")]


        pages = convert_from_path(caminhoPasta+"\\"+str(planNCT.loc[linha, 'NFE'])+" FCP.pdf", dpi=500, poppler_path=r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\poppler-24.08.0\Library\bin')
        print(caminhoPasta+"\\"+str(planNCT.loc[linha, 'NFE'])+" FCP.pdf")

        savegnre = pastapng + "\\" + str(planNCT.loc[linha, 'NFE'])

        for page in pages:
            page.save(savegnre+" FCP.png", 'PNG')

        frame = cv2.imread(savegnre+" FCP.png")
        detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

        if not detectedBarcode:
            print("Código de barras nao lida")
            planNCT["Cód Barra FCP"] = "Código de barras nao lida"
            linhaSpecif = planNCT.index == linha
            planNCT.loc[linhaSpecif, ["Cód Barra FCP"]] = "Código de barras nao lida"

        else:
            for barcode in detectedBarcode:
                if barcode.data != "":
                    print(barcode.data.decode("UTF-8"))
                    linhaSpecif = planNCT.index == linha
                    planNCT.loc[linhaSpecif, ["Cód Barra FCP"]] = [barcode.data.decode("UTF-8")]

    
    else:

        pages = convert_from_path(caminhoPasta+"\\"+str(planNCT.loc[linha, 'NFE'])+".pdf", dpi=500, poppler_path=r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\poppler-24.08.0\Library\bin')
        print(caminhoPasta+"\\"+str(planNCT.loc[linha, 'NFE'])+".pdf")

        savegnre = pastapng + "\\" + str(planNCT.loc[linha, 'NFE'])

        for page in pages:
            page.save(savegnre+".png", 'PNG')

        frame = cv2.imread(savegnre+".png")
        detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

        if not detectedBarcode:
            print("Código de barras nao lida")
            linhaSpecif = planNCT.index == linha
            planNCT.loc[linhaSpecif, ["Cód Barra"]] = "Código de barras nao lida"

        else:
            for barcode in detectedBarcode:
                if barcode.data != "":
                    print(barcode.data.decode("UTF-8"))
                    linhaSpecif = planNCT.index == linha
                    planNCT.loc[linhaSpecif, ["Cód Barra"]] = [barcode.data.decode("UTF-8")]

    linha = linha + 1
                
    

planNCT.drop(['Nota fiscal eletrônica',
            'Referência fiscal',
            'Status transmissão',
            'Tipo doc. fiscal',
            'Departamento',
            'Parc. Negócios NF Fatura',
            'Tipo identificador fiscal',
            ],
             axis=1, inplace=True)

planNCT.to_excel(
                r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\arquivo-nao-contribuinte\NCT cód barras.xlsx", index=False)