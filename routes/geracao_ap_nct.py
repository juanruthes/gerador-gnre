from flask import Blueprint, render_template, request
import pyautogui as pa
import time
from datetime import date, datetime
import pyperclip
import pandas as pd

geracao_ap_nct_route = Blueprint('geracao_ap_nct', __name__)

caminhoPasta = r"U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE"
dias = pd.Timedelta(days=12)

@ geracao_ap_nct_route.route("/gerar-ap-nct", methods=["POST"])
def gerar_ap_nct():
    time.sleep(0.5)

    pa.PAUSE = 0.8

    aprovador = request.form.get('check-aprovador')
    print(aprovador)

    if aprovador == "marco-alves":
        aprovadorNumero = "013078"
    elif aprovador == "otavio-mazzarolo":
        aprovadorNumero = "013033"
    elif aprovador == "stefan-rosiak":
        aprovadorNumero = "001547"
    
    print(aprovadorNumero)

    naoContribuintesDia = pd.read_excel(
        "static/data/arquivo-nao-contribuinte/Não Contribuintes.xlsx", dtype=str)
    
    #formatando data como DD/MM/AAAA
    naoContribuintesDia["Data de emissão"] = pd.to_datetime(naoContribuintesDia["Data de emissão"])
    naoContribuintesDia["Data de emissão"] = naoContribuintesDia["Data de emissão"].dt.strftime('%d/%m/%Y')

    naoContribuintesDia["Data de vencimento"] = pd.to_datetime(naoContribuintesDia["Data de vencimento"])
    naoContribuintesDia["Data de vencimento"] = naoContribuintesDia["Data de vencimento"].dt.strftime('%d/%m/%Y')

    dataEmissao = naoContribuintesDia['Data de emissão']
    dataVencimento = naoContribuintesDia['DT Venc LN']
    print(dataVencimento)
    
    naoContribuintesDia['Mês Referencia'] = naoContribuintesDia['Mês Referencia'].astype(
        'string')
    naoContribuintesDia['Ano Referencia'] = naoContribuintesDia['Ano Referencia'].astype(
        'string')

    codigoUF = naoContribuintesDia['UF']
    codigoFilial = naoContribuintesDia['Departamento']

    # naoContribuintesDia['Mês Referencia'] = naoContribuintesDia['Mês Referencia'].astype(
    #     'string')
    
    mesRef = naoContribuintesDia['Mês Referencia']

    linha = 0

    pa.hotkey('ctrl', 't')
    pa.moveTo(x=928, y=62)
    pa.click()
    pa.write(
        "http://ln.troxbrasil.com.br:8312/webui/servlet/standalone")
    pa.press("enter")
    time.sleep(3)
    pa.moveTo(x=30, y=167)
    pa.click()
    pa.press("tab")
    pa.write("tfzcpc103mt00")
    pa.press("enter")
    time.sleep(5)
    pa.moveTo(x=129, y=316)
    pa.click()
    pa.moveTo(x=30, y=167)
    pa.click()

    for linha in naoContribuintesDia.index:

        if codigoUF[linha] == "AL":
            pa.moveTo(x=132, y=197)
            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição

            pa.press("tab")

            pa.write(str(aprovadorNumero))  # Aprovador
            pa.press("tab")
            pa.press("tab")
            pa.write(str("BR0000013"))
            pa.press("tab")
            tipoLanc = "IM0002"  # Impostos e taxas estaduais
            pa.write(str(tipoLanc))  # Tipo de lançamento
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("BR0202"))
            else:
                pa.write(str("BR0102"))

            pa.press("tab")
            # Nota Fiscal
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.press("space")
            pa.press("tab")
            time.sleep(1)
            # Data de vencimento campo prioridade
            pa.write(str("VENC: " + naoContribuintesDia.loc[linha, "Data de vencimento"]))
            pa.press("tab")
            time.sleep(0.5)
            pa.press("tab")
            time.sleep(2)
            pa.moveTo(x=31, y=661)  # Criar linha dentro da AP
            pa.click()
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.write(str(naoContribuintesDia.loc[linha, "Data de emissão"]))
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("IMP000005"))
            else:
                pa.write(str("IMP000003"))

            pa.press("tab")
            pa.write(str("1"))
            pa.press("tab")
            # Valor
            pa.write(str(naoContribuintesDia.loc[linha, "Valor UF Destino"]))
            pa.press("tab")
            pa.press("tab")
            pa.write(str("BR1104"))
            pa.press("tab")

            pa.moveTo(x=143, y=630) 
            pa.click()
            pa.moveTo(x=41, y=705)  # Programação de pagamento
            pa.click()
            pa.press("del")
            pa.moveTo(x=860, y=673)
            pa.click()
            pa.press("enter")
            time.sleep(2)

            pa.moveTo(x=22, y=650)
            pa.click()


            pa.moveTo(x=100, y=705)
            pa.click()

            pa.write(str(naoContribuintesDia.loc[linha, 'DT Venc LN']))

            pa.press("tab")
            pa.moveTo(x=32, y=194)  # Sair salvando
            pa.click()

            # Fundo de combate a pobreza
            pa.moveTo(x=132, y=197)

            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição

            pa.press("tab")

            pa.write(str(aprovadorNumero))  # Aprovador
            pa.press("tab")
            pa.press("tab")
            pa.write(str("BR0000013"))
            pa.press("tab")
            tipoLanc = "IM0002"  # Impostos e taxas estaduais
            pa.write(str(tipoLanc))  # Tipo de lançamento
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("BR0202"))
            else:
                pa.write(str("BR0102"))

            pa.press("tab")
            # Nota Fiscal
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("tab")
            pa.write(str("FCP"))  # apagar
            pa.press("tab")  # apagar
            pa.press("tab")
            pa.press("tab")
            pa.press("space")
            pa.press("tab")
            time.sleep(1)
            # Data de vencimento campo prioridade
            pa.write(str("VENC: " + naoContribuintesDia.loc[linha, "Data de vencimento"]))
            pa.press("tab")
            time.sleep(0.5)
            pa.press("tab")
            time.sleep(2)
            pa.moveTo(x=31, y=661)  # Criar linha dentro da AP
            pa.click()
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.write(str(naoContribuintesDia.loc[linha, "Data de emissão"]))
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("IMP000005"))
            else:
                pa.write(str("IMP000003"))

            pa.press("tab")
            pa.write(str("1"))
            pa.press("tab")
            # Valor
            pa.write(
                str(naoContribuintesDia.loc[linha, "Valor FCP"]))
            pa.press("tab")
            pa.press("tab")
            pa.write(str("BR1104"))
            pa.press("tab")

            pa.moveTo(x=143, y=630) 
            pa.click()
            pa.moveTo(x=41, y=705)  # Programação de pagamento
            pa.click()
            pa.press("del")
            pa.moveTo(x=860, y=673)
            pa.click()
            pa.press("enter")
            time.sleep(2)

            pa.moveTo(x=22, y=650)
            pa.click()
            pa.moveTo(x=100, y=705)
            pa.click()


            pa.write(str(naoContribuintesDia.loc[linha, 'DT Venc LN']))

            pa.press("tab")

            pa.moveTo(x=32, y=194)  # Sair salvando
            pa.click()

        else:
            pa.moveTo(x=132, y=197)

            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição

            pa.press("tab")

            pa.write(str(aprovadorNumero))  # Aprovador
            pa.press("tab")
            pa.press("tab")

            if codigoUF[linha] == "PR":
                # PN da UF
                pa.write(str("BR0000003"))
            elif codigoUF[linha] == "SP":
                # PN da UF
                pa.write(str("BR0000004"))
            elif codigoUF[linha] == "SC":
                # PN da UF
                pa.write(str("BR0000005"))
            elif codigoUF[linha] == "RS":
                # PN da UF
                pa.write(str("BR0000006"))
            elif codigoUF[linha] == "AC":
                # PN da UF
                pa.write(str("BR0000007"))
            elif codigoUF[linha] == "AP":
                # PN da UF
                pa.write(str("BR0000008"))
            elif codigoUF[linha] == "MG":
                # PN da UF
                pa.write(str("BR0000009"))
            elif codigoUF[linha] == "PE":
                # PN da UF
                pa.write(str("BR0000010"))
            elif codigoUF[linha] == "RR":
                # PN da UF
                pa.write(str("BR0000011"))
            elif codigoUF[linha] == "SE":
                # PN da UF
                pa.write(str("BR0000012"))
            elif codigoUF[linha] == "AL":
                # PN da UF
                pa.write(str("BR0000013"))
            elif codigoUF[linha] == "AM":
                # PN da UF
                pa.write(str("BR0000014"))
            elif codigoUF[linha] == "BA":
                # PN da UF
                pa.write(str("BR0000015"))
            elif codigoUF[linha] == "CE":
                # PN da UF
                pa.write(str("BR0000016"))
            elif codigoUF[linha] == "DF":
                # PN da UF
                pa.write(str("BR0000017"))
            elif codigoUF[linha] == "ES":
                # PN da UF
                pa.write(str("BR0000018"))
            elif codigoUF[linha] == "GO":
                # PN da UF
                pa.write(str("BR0000019"))
            elif codigoUF[linha] == "MA":
                # PN da UF
                pa.write(str("BR0000020"))
            elif codigoUF[linha] == "MT":
                # PN da UF
                pa.write(str("BR0000021"))
            elif codigoUF[linha] == "MS":
                # PN da UF
                pa.write(str("BR0000022"))
            elif codigoUF[linha] == "PA":
                # PN da UF
                pa.write(str("BR0000023"))
            elif codigoUF[linha] == "PB":
                # PN da UF
                pa.write(str("BR0000024"))
            elif codigoUF[linha] == "PI":
                # PN da UF
                pa.write(str("BR0000025"))
            elif codigoUF[linha] == "RJ":
                # PN da UF
                pa.write(str("BR0000026"))
            elif codigoUF[linha] == "RN":
                # PN da UF
                pa.write(str("BR0000027"))
            elif codigoUF[linha] == "RO":
                # PN da UF
                pa.write(str("BR0000028"))
            elif codigoUF[linha] == "TO":
                # PN da UF
                pa.write(str("BR0000029"))

            pa.press("tab")
            tipoLanc = "IM0002"  # Impostos e taxas estaduais
            pa.write(str(tipoLanc))  # Tipo de lançamento
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("BR0202"))
            else:
                pa.write(str("BR0102"))

            pa.press("tab")
            # Nota Fiscal
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.press("space")
            pa.press("tab")
            time.sleep(1)
            # Data de vencimento campo prioridade
            pa.write(str("VENC: " + naoContribuintesDia.loc[linha, "Data de vencimento"]))
            pa.press("tab")
            time.sleep(0.5)
            pa.press("tab")
            time.sleep(2)
            pa.moveTo(x=31, y=661)  # Criar linha dentro da AP
            pa.click()
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")
            pa.write(str(naoContribuintesDia.loc[linha, "Data de emissão"]))
            pa.press("tab")
            pa.press("tab")
            pa.press("tab")

            if codigoFilial[linha] == "BR0201":  # Tipo de lançamento
                # PN da UF
                pa.write(str("IMP000005"))
            else:
                pa.write(str("IMP000003"))

            pa.press("tab")
            pa.write(str("1"))
            pa.press("tab")
            # Valor
            pa.write(str(naoContribuintesDia.loc[linha, "Valor Total DIFAL"]))
            pa.press("tab")
            pa.press("tab")
            pa.write(str("BR1104"))
            pa.press("tab")

            pa.moveTo(x=143, y=630) 
            pa.click()
            pa.moveTo(x=41, y=705)  # Programação de pagamento
            pa.click()
            pa.press("del")
            pa.moveTo(x=860, y=673)
            pa.click()
            pa.press("enter")
            time.sleep(2)

            pa.moveTo(x=22, y=650)
            pa.click()
            pa.moveTo(x=100, y=705)
            pa.click()

            pa.write(str(naoContribuintesDia.loc[linha, 'DT Venc LN']))

            
            pa.press("tab")
   
            pa.moveTo(x=32, y=194)  # Sair salvando
            pa.click()

    pa.moveTo(x=1893, y=137)
    pa.click()
    time.sleep(1)

    # Salvando GNREs

    for linha in naoContribuintesDia.index:

        if codigoUF[linha] == "AL":
            pa.moveTo(x=654, y=270)  # pesquisar gnre 
            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição

            pa.press("tab")

            pa.moveTo(x=43, y=290)
            pa.click()

            pa.moveTo(x=1689, y=198)
            pa.click()

            pa.moveTo(x=1777, y=235)
            pa.click()

            pa.moveTo(x=480, y=700)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=847, y=56) #Pesquisar caminho pasta
            pa.click()

            if mesRef[linha] == "01":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "02":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")      
            elif mesRef[linha] == "03":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "04":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "05":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "06":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "07":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "08":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "09":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")        
            elif mesRef[linha] == "10":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "11":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "12":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")

            pa.press("enter")

            pa.moveTo(x=1021, y=59) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("enter")
            pa.moveTo(x=435, y=201)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=19, y=205)
            pa.click()
            time.sleep(3)

            pa.moveTo(x=935, y=205)
            pa.click()
            time.sleep(10)
     

            # Fundo de combate a pobreza
            pa.moveTo(x=654, y=270)  # pesquisar gnre
            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"] + " - FCP"))  # Descrição
            pa.press("tab")

            pa.moveTo(x=43, y=290)
            pa.click()

            pa.moveTo(x=1689, y=198)
            pa.click()

            pa.moveTo(x=1777, y=235)
            pa.click()

            pa.moveTo(x=480, y=700)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=847, y=56) #Pesquisar caminho pasta
            pa.click()

            if mesRef[linha] == "01":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "02":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")      
            elif mesRef[linha] == "03":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "04":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "05":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "06":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "07":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "08":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "09":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")        
            elif mesRef[linha] == "10":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "11":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "12":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")

            pa.press("enter")
            pa.moveTo(x=1021, y=59) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"] + " FCP"))
            pa.press("enter")
            pa.moveTo(x=354, y=146)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=19, y=205)
            pa.click()
            time.sleep(3)


            pa.moveTo(x=935, y=205)
            pa.click()
            time.sleep(10)

        else:
            pa.moveTo(x=654, y=270)  # pesquisar gnre
            time.sleep(1)
            pa.click()
            time.sleep(1)

            if codigoFilial[linha] == "BR0201":
                pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0101":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0103":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0104":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            elif codigoFilial[linha] == "BR0105":
                pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
                    naoContribuintesDia.loc[linha, "UF"]))  # Descrição
            pa.press("tab")

            pa.moveTo(x=43, y=290)
            pa.click()

            pa.moveTo(x=1689, y=198)
            pa.click()

            pa.moveTo(x=1777, y=235)
            pa.click()

            pa.moveTo(x=480, y=700)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=847, y=56) #Pesquisar caminho pasta
            pa.click()

            if mesRef[linha] == "01":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "02":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")      
            elif mesRef[linha] == "03":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "04":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "05":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "06":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "07":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "08":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "09":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")        
            elif mesRef[linha] == "10":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "11":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")
            elif mesRef[linha] == "12":
                textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
                pyperclip.copy(textCopy)
                pa.hotkey("ctrl", "v")

            pa.press("enter")
            pa.moveTo(x=1021, y=59) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("enter")
            pa.moveTo(x=378, y=137)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=19, y=205)
            pa.click()

            time.sleep(3)
            pa.moveTo(x=935, y=205)
            pa.click()
            time.sleep(8)

    pa.moveTo(x=1893, y=137)
    pa.click()
    time.sleep(1)
    pa.hotkey("ctrl", "w")
    pa.hotkey("enter")

    msg3 = "Lançamento das aps concluídas"

    return render_template("nao-contribuintes.html", msg=msg3)
