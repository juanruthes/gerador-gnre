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



print(request.form.get('vencimento-data'))

data_venc = request.form.get('vencimento-data')

linhas_nfe = pd.read_excel("data/Linhas_da_NFE_ST.xlsx")

cadastro = pd.read_excel("data/Parceiro de negocios.xlsx")

tabela_cest = pd.read_excel()

linhas_nfe.drop(['Import Status',
                'Import Code',
                    'Import Message',
                    'Companhia',
                    'Data de emissão',
                    'Até',
                    'Localização',
                    'Gerar agenda',
                    'Código do tipo de doc. fiscal',
                    'Descrição',
                    'Item',
                    'Referência',
                    'Natureza da operação',
                    'Tipo doc. fiscal',
                    'Quantidade',
                    'Preço',
                    'Valor líquido',
                    'Valor mercadoria',
                    'Valor',
                    'Linhas',
                    'Tipo',
                    'IPI',
                    'PIS',
                    'COFINS',
                    'IRRF pessoa jurídica',
                    'PIS retido',
                    'COFINS retido',
                    'CSLL retido',
                    'ISS',
                    'ISS retido',
                    'INSS retido pessoa jurídica',
                    'Base UF Destinatário',
                    'Alíquota Interna Destinatário',
                    'Alíquota Interestadual',
                    'Percentual Fundo Combate Pobreza (adicionado à aliquota)',
                    'Representante de vendas',
                    'Nome',
                    'Fator de venda',
                    'Conta contábil',
                    'NF manual',
                    'Nota fiscal eletrônica',
                    'Frete',
                    'Seguro na moeda cia.',
                    'Despesas gerais',
                    'Prioridade',
                    'Transportadora',
                    'Nome transportadora',
                    'Beneficio Fiscal na UF',
                    'Código FCI',
                    'Origem mercadoria',
                    'Percentual de comissão',
                    'Documento Contab.',
                    'Descrição.1',
                    'Unnamed: 28',
                    'Unnamed: 21',
                    'Valor UF Remetente',
                    'Unnamed: 67',
                    'ICMS',
                    'Unnamed: 73',
                    ],
                axis=1, inplace=True)
linhas_nfe

# Somando os valores de Difal e FCP

linhas_nfe_difal = linhas_nfe.groupby(["Referência fiscal", "Número do documento", "Departamento", "PN", "Razão Social", "Estado", "CNPJ Parceiro"]).agg({
    'Valor UF Destino': 'sum', 'Valor Fundo Combate Pobreza': 'sum'}).reset_index()
linhas_nfe_difal

# Deletando departamento BR0501 - Ecommerce

linhas_nfe_difal = linhas_nfe_difal[(
    linhas_nfe_difal[['Departamento']] != "BR0501").all(axis=1)]
linhas_nfe_difal

linhas_nfe_difal['Valor Total DIFAL'] = linhas_nfe_difal['Valor UF Destino'] + \
    linhas_nfe_difal["Valor Fundo Combate Pobreza"]
linhas_nfe_difal

# Deletando linhas cujo "Valor UF destino" é zero
linhas_nfe_difal = linhas_nfe_difal[(
    linhas_nfe_difal[['Valor Total DIFAL']] != 0).all(axis=1)]
linhas_nfe_difal

# Tratamento com a planilha Nota Fiscal

notafiscal = pd.read_excel("data/Nota_Fiscal.xlsx")

notafiscal.drop(['Import Status',
                'Import Code',
                    'Import Message',
                    'Companhia',
                    'Data de saída',
                    'Numero NFSe',
                    'CFO',
                    'Status da fatura',
                    'Status da NF-e',
                    'NF manual',
                    'Valor total',
                    'Valor total da agenda',
                    'Protocolo NF-e',
                    'Código da razão cancelamento',
                    'Req.faturamento',
                    'Modalidade do Frete',
                    'Terceiros 2 NF',
                    'Cond. de entrega',
                    'Cond de pag',
                    'Transportadora',
                    'Endereço para faturamento',
                    'PN receptor',
                    'Código do tipo de doc. fiscal',
                    'Unnamed: 32',
                    'Unnamed: 20',
                    'Consumidor final',
                    ],
                axis=1, inplace=True)
notafiscal

# Deletando "Prestação de serviço" e "Ecommerce"

notafiscal = notafiscal[(notafiscal[['Tipo doc. fiscal']]
                        != "Prestação de serviços").all(axis=1)]
notafiscal
notafiscal = notafiscal[(
    notafiscal[['Departamento']] != "BR0501").all(axis=1)]
notafiscal

# Tratamento com a planilha Cadastro

cadastro
cadastro.drop(['Import Status',
                'Import Code',
                'Import Message',
                'Companhia',
                'Endereço',
                'Status',
                'Unnamed: 10',
                'CEP/Código postal',
                'País',
                'Moeda',
                'Número local',
                'Cargo',
                'Número de telefone',
                'A ser verificado',
                'Parceiro de negócios pai',
                'Unnamed: 21',
                ],
                axis=1, inplace=True)
cadastro

cadastro['Parceiro de negócios'] = cadastro['Parceiro de negócios'].astype(
    'string')
cadastro

notafiscal['Referência fiscal'] = notafiscal['Referência fiscal'].astype(
    'string')
notafiscal

linhas_nfe_difal['Referência fiscal'] = linhas_nfe_difal['Referência fiscal'].astype(
    'string')
linhas_nfe_difal

# Junção das planilhas "Parceiro de negócios" e "Linhas da nota fiscal", usando como base a plan "Nota Fiscal"

notafiscal = notafiscal.merge(cadastro,
                                left_on='Parceiro de negócios faturado',
                                right_on='Parceiro de negócios',
                                how='outer')
notafiscal

notafiscal = notafiscal.merge(linhas_nfe_difal,
                                left_on='Referência fiscal',
                                right_on='Referência fiscal',
                                how='outer')
notafiscal

# Deletando linhas que possui "NaN" na coluna "Valor UF destino"

notafiscal = notafiscal.dropna(subset=['ICMS ST'])
notafiscal
notafiscal.drop(['Parceiro de negócios',
                'Unnamed: 5',
                    'Endereço.1',
                    'Número do documento_y',
                    'Departamento_y',
                    'PN',
                    'Razão Social',
                    'Estado',
                    'CNPJ Parceiro',
                    ],
                axis=1, inplace=True)
notafiscal

# Tratamento das colunas "Data de emissao, Entidade Fiscal, Cidade"

notafiscal['Data de emissão'] = notafiscal['Data de emissão'].astype(
    'datetime64[ns]')
notafiscal
notafiscal['Entidade fiscal'] = notafiscal['Entidade fiscal'].astype(
    'string')
notafiscal
notafiscal['Cidade'] = notafiscal['Cidade'].astype('string')
notafiscal
notafiscal['Departamento_x'] = notafiscal['Departamento_x'].astype(
    'string')
notafiscal

# Tratamento do campo Entidade Fiscal

notafiscal['Entidade fiscal'] = notafiscal['Entidade fiscal'].str.replace(
    '-', '').str.replace('/', '')
notafiscal

# Tratamento do string para o Campo "Cidade", que de acordo com o XML do Portal GNRE, os dois primeiros numeros do IBGE precisam ser removidos

notafiscal['Cidade'] = notafiscal['Cidade'].str[2:]
notafiscal

notafiscal['Valor Total DIFAL'] = notafiscal['Valor UF Destino'] + \
    notafiscal['Valor Fundo Combate Pobreza']
notafiscal

notafiscal['Data de emissão'] = notafiscal['Data de emissão'].astype(
    'string')
notafiscal

notafiscal['Data de emissão'] = notafiscal['Data de emissão'].str[:10]
notafiscal

# Inserindo Mes e Ano de Referencia na Planilha

notafiscal["Mês Referencia"] = notafiscal["Data de emissão"].str[5:7]
notafiscal
notafiscal["Ano Referencia"] = notafiscal["Data de emissão"].str[:4]
notafiscal

notafiscal['ICMS ST'] = notafiscal['ICMS ST'].map(
    '{:.2f}'.format)
notafiscal

notafiscal = notafiscal.dropna(subset=["Parceiro de negócios faturado"])
notafiscal

notafiscal = notafiscal[(   
    notafiscal[['Estado/Município']] != "SP").all(axis=1)]
notafiscal

notafiscal = notafiscal[(
    notafiscal[['Estado/Município']] != "PE").all(axis=1)]
notafiscal

notafiscal["Data de vencimento"] = pd.to_datetime(data_venc)
notafiscal["Data de vencimento"] = notafiscal["Data de vencimento"].dt.strftime('%Y-%m-%d')

notafiscal = notafiscal.rename(columns={"NFE":"NFE", "Unnamed: 12":"Razão Social", "Departamento_x":"Departamento", "Estado/Município": "UF", "Parceiro de negócios faturado":"PN", "Número do documento_x":"NFE", "Valor Fundo Combate Pobreza":"Valor FCP"})


notafiscal.to_excel("static/data/arquivo-nao-contribuinte/Não Contribuintes.xlsx", index=False)

# Tratamento da segunda planilha
nfe_table = pd.read_excel("static/data/arquivo-nao-contribuinte/Não Contribuintes.xlsx")

nfe_table.drop(['Referência fiscal', 'Nota fiscal eletrônica',
                'Status transmissão', 'Tipo doc. fiscal', 'Departamento', 'Localizador', 'Entidade fiscal', 'Cidade', 'Tipo identificador fiscal', 'Mês Referencia', 'Ano Referencia', 'Parc. Negócios NF Fatura'],
                axis=1, inplace=True)
nfe_table

#formatando data como DD/MM/AAAA
nfe_table['Valor UF Destino'] = nfe_table['Valor UF Destino'].map(
    '{:_.2f}'.format)
nfe_table
nfe_table['Valor FCP'] = nfe_table['Valor FCP'].map(
    '{:_.2f}'.format)
nfe_table
nfe_table['Valor Total DIFAL'] = nfe_table['Valor Total DIFAL'].map(
    '{:_.2f}'.format)
nfe_table

nfe_table['Valor UF Destino'] = nfe_table['Valor UF Destino'].str.replace('.',',').str.replace('_','.')
nfe_table['Valor FCP'] = nfe_table['Valor FCP'].str.replace('.',',').str.replace('_','.')
nfe_table['Valor Total DIFAL'] = nfe_table['Valor Total DIFAL'].str.replace('.',',').str.replace('_','.')


nfe_table["Data de emissão"] = pd.to_datetime(nfe_table["Data de emissão"])

nfe_table["Data de emissão"] = nfe_table["Data de emissão"].dt.strftime('%d/%m/%Y')

nfe_table["Data de vencimento"] = pd.to_datetime(nfe_table["Data de vencimento"])

nfe_table["Data de vencimento"] = nfe_table["Data de vencimento"].dt.strftime('%d/%m/%Y')


#Gerando XML


#Gerando visual tabela
nfe_table.to_excel(
    "static/data/Guias ST Visual.xlsx", index=False)

nfe_table2 = pd.read_excel(
    "static/data/Guias ST.xlsx")

nfe_table2

