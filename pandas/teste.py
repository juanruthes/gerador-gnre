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


pages = convert_from_path("U:\\Contabilidade\\Movimento.Diario\\Impostos e Contribuições\\GNRE 2025\\08. ARQUIVO GNRE AGO 2025\\101622 ST.pdf", dpi=500, poppler_path=r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\poppler-24.08.0\Library\bin')

pastapng = r"static\data\gnre"
savegnre = pastapng + "\\" + "101622 ST"

for page in pages:
    page.save(savegnre+".png", 'PNG')

frame = cv2.imread(savegnre+".png")
detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

if not detectedBarcode:
    print("Código de barras nao lida")


else:
    for barcode in detectedBarcode:
        if barcode.data != "":
            print(barcode.data.decode("UTF-8"))
