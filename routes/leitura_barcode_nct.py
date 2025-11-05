import os
import pandas as pd
from pdf2image import convert_from_path
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
from flask import Blueprint, render_template, request
from pathlib import Path

ler_barcode_nct_route = Blueprint('ler_barcode_nct', __name__)

@ ler_barcode_nct_route.route("/ler-barcode-nct", methods=["GET", "POST"])
def ler_barcode_nct():
    
    caminhoPasta = Path("U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE")
    planNCT = pd.read_excel("static\\data\\arquivo-nao-contribuinte\\Não Contribuintes.xlsx")
    pastapng = r"static\data\gnre"

    linha = 0

    mesRef = planNCT["Mês Referencia"]
    print(mesRef)

    meses_abrev = {
        "01": "JAN",
        "02": "FEV",
        "03": "MAR",
        "04": "ABR",
        "05": "MAI",
        "06": "JUN",
        "07": "JUL",
        "08": "AGO",
        "09": "SET",
        "10": "OUT",
        "11": "NOV",
        "12": "DEZ"
    }

    # Garantindo que o mês tenha dois dígitos
    mes = str(mesRef[linha]).zfill(2)
    ano = planNCT.loc[linha, "Ano Referencia"]
    mes_completo = planNCT.loc[linha, "Mês Referencia"]
    abrev_mes = meses_abrev.get(mes, "MÊS_INVÁLIDO")

    # Montando o caminho
    caminhoPastaGNRE = f'{caminhoPasta} {ano}\\{mes}. ARQUIVO GNRE {abrev_mes} {ano}'

    if os.path.exists(caminhoPastaGNRE):
        for unidadeFederativa in planNCT['UF']:
            try:
                nfe = str(planNCT.loc[linha, 'NFE'])
                pdf_path = os.path.join(caminhoPastaGNRE, f"{nfe}.pdf")

                if unidadeFederativa == "AL":
                    if not os.path.exists(pdf_path):
                        print(f"Arquivo não encontrado: {pdf_path}")
                        planNCT.loc[linha, ["Cód Barra"]] = "Arquivo não encontrado"
                    else:
                        # Processa GNRE normal
                        try:
                            pages = convert_from_path(pdf_path, dpi=500, poppler_path=r'poppler-24.08.0\Library\bin')
                            savegnre = os.path.join(pastapng, nfe)

                            for page in pages:
                                page.save(savegnre + ".png", 'PNG')

                            frame = cv2.imread(savegnre + ".png")
                            detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

                            if not detectedBarcode:
                                print("Código de barras não lido")
                                planNCT.loc[linha, ["Cód Barra"]] = "Código de barras nao lida"
                            else:
                                for barcode in detectedBarcode:
                                    if barcode.data:
                                        decoded = barcode.data.decode("UTF-8")
                                        print(decoded)
                                        planNCT.loc[linha, ["Cód Barra"]] = decoded
                        except Exception as e:
                            print(f"Erro ao processar GNRE: {e}")
                            planNCT.loc[linha, ["Cód Barra"]] = "Erro ao processar"

                    # Processa FCP
                    fcp_pdf_path = os.path.join(caminhoPastaGNRE, f"{nfe} FCP.pdf")
                    if not os.path.exists(fcp_pdf_path):
                        print(f"Arquivo não encontrado: {fcp_pdf_path}")
                        planNCT.loc[linha, ["Cód Barra FCP"]] = "Arquivo não encontrado"
                    else:
                        try:
                            pages = convert_from_path(fcp_pdf_path, dpi=500, poppler_path=r'poppler-24.08.0\Library\bin')
                            savegnre_fcp = os.path.join(pastapng, nfe) + " FCP"

                            for page in pages:
                                page.save(savegnre_fcp + ".png", 'PNG')

                            frame = cv2.imread(savegnre_fcp + ".png")
                            detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

                            if not detectedBarcode:
                                print("Código de barras FCP não lido")
                                planNCT.loc[linha, ["Cód Barra FCP"]] = "Código de barras nao lida"
                            else:
                                for barcode in detectedBarcode:
                                    if barcode.data:
                                        decoded = barcode.data.decode("UTF-8")
                                        print(decoded)
                                        planNCT.loc[linha, ["Cód Barra FCP"]] = decoded
                        except Exception as e:
                            print(f"Erro ao processar FCP: {e}")
                            planNCT.loc[linha, ["Cód Barra FCP"]] = "Erro ao processar"

                else:
                    if not os.path.exists(pdf_path):
                        print(f"Arquivo não encontrado: {pdf_path}")
                        planNCT.loc[linha, ["Cód Barra"]] = "Arquivo não encontrado"
                    else:
                        try:
                            pages = convert_from_path(pdf_path, dpi=500, poppler_path=r'poppler-24.08.0\Library\bin')
                            savegnre = os.path.join(pastapng, nfe)

                            for page in pages:
                                page.save(savegnre + ".png", 'PNG')

                            frame = cv2.imread(savegnre + ".png")
                            detectedBarcode = decode(frame, symbols=[ZBarSymbol.I25])

                            if not detectedBarcode:
                                print("Código de barras não lido")
                                planNCT.loc[linha, ["Cód Barra"]] = "Código de barras nao lida"
                            else:
                                for barcode in detectedBarcode:
                                    if barcode.data:
                                        decoded = barcode.data.decode("UTF-8")
                                        print(decoded)
                                        planNCT.loc[linha, ["Cód Barra"]] = decoded
                        except Exception as e:
                            print(f"Erro ao processar GNRE: {e}")
                            planNCT.loc[linha, ["Cód Barra"]] = "Erro ao processar"

            except Exception as e:
                print(f"Erro geral na linha {linha}: {e}")
                planNCT.loc[linha, ["Cód Barra"]] = "Erro inesperado"

            linha += 1

    else:
        linhaSpecif = planNCT.index == linha
        planNCT.loc[linhaSpecif, ["Cód Barra"]] = "Pasta GNRE não encontrada"
        linha += 1

    planNCT.drop(['Nota fiscal eletrônica',
                'Referência fiscal',
                'Status transmissão',
                'Tipo doc. fiscal',
                'Departamento',
                'Parc. Negócios NF Fatura',
                'Tipo identificador fiscal',
                'Localizador',
                'Entidade fiscal',
                'Cidade',
                'PN',
                'Razão Social'
                ],
                axis=1, inplace=True)
    
    planNCT = planNCT.fillna('-')

    planNCT["Data de emissão"] = pd.to_datetime(planNCT["Data de emissão"])
    planNCT["Data de emissão"] = planNCT["Data de emissão"].dt.strftime('%d/%m/%Y')

    planNCT["Data de vencimento"] = pd.to_datetime(planNCT["Data de vencimento"])
    planNCT["Data de vencimento"] = planNCT["Data de vencimento"].dt.strftime('%d/%m/%Y')
           
    planNCT['Valor UF Destino'] = planNCT['Valor UF Destino'].map(
        '{:_.2f}'.format)
    planNCT['Valor UF Destino'] = planNCT['Valor UF Destino'].str.replace('.',',').str.replace('_','.')
    planNCT['Valor FCP'] = planNCT['Valor FCP'].map(
        '{:_.2f}'.format)
    planNCT['Valor FCP'] = planNCT['Valor FCP'].str.replace('.',',').str.replace('_','.')
    planNCT['Valor Total DIFAL'] = planNCT['Valor Total DIFAL'].map(
        '{:_.2f}'.format)
    planNCT['Valor Total DIFAL'] = planNCT['Valor Total DIFAL'].str.replace('.',',').str.replace('_','.')
 
    planNCT = planNCT.rename(columns={"Valor UF Destino":"UF Dest.", "Valor FCP":"FCP", "Valor Total DIFAL":"DIFAL", "Mês Referencia": "Mês", "Ano Referencia":"Ano", "Data de vencimento":"Vencimento", 
                                      "Valor FCP":"FCP", "Data de emissão":"Data"})

    planNCT.to_excel("static\\data\\arquivo-nao-contribuinte\\Não Contribuintes código de barras.xlsx", index=False)
    
    mensagem2 = "Planilha pronta para download"

    nfe_table2 = pd.read_excel("static\\data\\arquivo-nao-contribuinte\\Não Contribuintes código de barras.xlsx")


    def deletando_arquivos(folder_path):

        try:
            files = os.listdir(folder_path)
            if len(files) == 0:
                print(f"Sem arquivos a deletar")
            else:
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    print("Feito!")
        except OSError:
            print("Erro, verificar")


    deletando_arquivos(pastapng)
        
    return render_template("nao-contribuintes.html", tables2=[nfe_table2.to_html()], titles=[''], msg2=mensagem2)

