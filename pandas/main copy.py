import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import date, datetime
import pyautogui as pa
import time
import pyperclip
import xml.etree.ElementTree as ET
import pandas as pd

aprovador = "013033"

app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
DIRXML = "C:\\Users\\juan.santos\\Documents\\Juan\\Juan\\Gerador de GNRE\\static\\data\\xml"
DIRXLSX = "C:\\Users\\juan.santos\\Documents\\Juan\\Juan\\Gerador de GNRE\\Gerador de GNRE\\static\\data\\arquivo-nao-contribuinte"

caminhoPasta = r"U:\Contabilidade\Movimento.Diario\Impostos e Contribuições\GNRE"


@ app.route("/")
def index():
    return render_template("index.html")


@ app.route("/data", methods=["POST"])
def data_linhasnotafiscal():
    file = request.files["file-1"]
    file.filename = "Linhas da NFE.xlsx"
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)

    file = request.files["file-2"]
    file.filename = "Nota Fiscal.xlsx"
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)

    mensagem = "Arquivos salvos!"

    # Inserir mensagem abaixo da caixa
    return render_template("index.html", msg=mensagem)


@ app.route("/static/data/planilha-gerada", methods=["GET", "POST"])
def planilha_gerada():

    print(request.form.get('vencimento-data'))

    data_venc = request.form.get('vencimento-data')

    linhas_nfe = pd.read_excel(
        r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\data\Linhas_da_NFE.xlsx')

    cadastro = pd.read_excel(
        r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\data\Parceiro de negocios.xlsx')

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
                     'ICMS ST',
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

    notafiscal = pd.read_excel(
        r'C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\data\Nota_Fiscal.xlsx')

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

    notafiscal = notafiscal.dropna(subset=['Valor Total DIFAL'])
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

    notafiscal['Valor UF Destino'] = notafiscal['Valor UF Destino'].map(
        '{:.2f}'.format)
    notafiscal
    notafiscal['Valor Fundo Combate Pobreza'] = notafiscal['Valor Fundo Combate Pobreza'].map(
        '{:.2f}'.format)
    notafiscal
    notafiscal['Valor Total DIFAL'] = notafiscal['Valor Total DIFAL'].map(
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


    notafiscal.to_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx", index=False)

    # Tratamento da segunda planilha
    nfe_table = pd.read_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx")

    nfe_table.drop(['Referência fiscal', 'Nota fiscal eletrônica',
                    'Status transmissão', 'Tipo doc. fiscal', 'Departamento', 'Localizador', 'Entidade fiscal', 'Cidade', 'Tipo identificador fiscal', 'Mês Referencia', 'Ano Referencia', 'Parc. Negócios NF Fatura'],
                   axis=1, inplace=True)
    nfe_table
    
    #formatando data como DD/MM/AAAA
    nfe_table["Data de emissão"] = pd.to_datetime(nfe_table["Data de emissão"])

    nfe_table["Data de emissão"] = nfe_table["Data de emissão"].dt.strftime('%d/%m/%Y')

    nfe_table["Data de vencimento"] = pd.to_datetime(nfe_table["Data de vencimento"])

    nfe_table["Data de vencimento"] = nfe_table["Data de vencimento"].dt.strftime('%d/%m/%Y')


    #Gerando XML

    naoContribuintesDia = pd.read_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx", dtype=str)

    loteGNRE = ET.Element('TLote_GNRE')
    loteGNRE.attrib["versao"] = '2.00'
    loteGNRE.attrib["xmlns"] = 'http://www.gnre.pe.gov.br'
    guias = ET.SubElement(loteGNRE, 'guias')
    
    linha = 0

    for unidadeFederativa in naoContribuintesDia['UF']:

        if unidadeFederativa == "AL":
            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'AL'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '90'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data de pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # # GNRE 100129

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'AL'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100129'

            # Detalhamento da Receita
            receitaDetalhamento = ET.SubElement(item, 'detalhamentoReceita')
            receitaDetalhamento.text = '000079'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = str(
                naoContribuintesDia.loc[linha, "Valor FCP"])

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])
            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '90'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])
            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = naoContribuintesDia.loc[linha,
                                                     "Valor FCP"]
            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "AC":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'AC'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '120'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = naoContribuintesDia.loc[linha,
                                                     "Valor Total DIFAL"]

            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "AM":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'AM'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # itens GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '22'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaPeriodo = ET.SubElement(referencia, 'periodo')
            referenciaPeriodo.text = '0'
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])
            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = naoContribuintesDia.loc[linha,
                                                     "Valor Total DIFAL"]

            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "AP":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'AP'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            contribuinteEmitente = ET.SubElement(
                dadosGNRE, 'contribuinteEmitente')
            identificacao = ET.SubElement(
                contribuinteEmitente, 'identificacao')
            cnpj = ET.SubElement(identificacao, 'CNPJ')
            cnpj.text = '76881093000172'
            razaoSocial = ET.SubElement(contribuinteEmitente, 'razaoSocial')
            razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
            endereco = ET.SubElement(contribuinteEmitente, 'endereco')
            endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
            municipio = ET.SubElement(contribuinteEmitente, 'municipio')
            municipio.text = '06902'  # Curitiba
            uf = ET.SubElement(contribuinteEmitente, 'uf')
            uf.text = 'PR'
            cep = ET.SubElement(contribuinteEmitente, 'cep')
            cep.text = '81170230'
            telefone = ET.SubElement(contribuinteEmitente, 'telefone')
            telefone.text = '4133168400'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaPeriodo = ET.SubElement(referencia, 'periodo')
            referenciaPeriodo.text = '0'
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '47'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = naoContribuintesDia.loc[linha,
                                                     "Valor Total DIFAL"]

            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "BA":
            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'BA'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

        # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            referencia = ET.SubElement(item, 'referencia')
            referenciaPeriodo = ET.SubElement(referencia, 'periodo')
            referenciaPeriodo.text = '0'
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '86'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = naoContribuintesDia.loc[linha,
                                                     "Valor Total DIFAL"]
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "CE":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'CE'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Valor GNRE
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "GO":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'GO'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '102'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "MA":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'MA'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Produto
            produto = ET.SubElement(item, 'produto')
            produto.text = '89'

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '94'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data de pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "MG":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'MG'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data de pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "MS":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'MS'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '88'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data de pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "MT":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'MT'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Detalhamento da Receita
            receitaDetalhamento = ET.SubElement(item, 'detalhamentoReceita')
            receitaDetalhamento.text = '000055'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '22'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "PA":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'PA'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '101'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "PB":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'PB'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '99'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "PI":
            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'PI'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == 'RJ':

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            # UF Favorecida
            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'RJ'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '24'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])
            produto = ET.SubElement(item, 'produto')
            produto.text = '89'

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # number_string_vlFcp = naoContribuintesDia.loc[linha, "Valor FCP"]
            valorPagamentoFCP = str(naoContribuintesDia.loc[linha,
                                                            "Valor FCP"])

            # number_string_vlTotal = naoContribuintesDia.loc[linha, "Total"]
            valorTotal = str(naoContribuintesDia.loc[linha,
                                                     "Valor Total DIFAL"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            valorFCP = ET.SubElement(item, 'valor')
            valorFCP.attrib["tipo"] = '12'
            valorFCP.text = valorPagamentoFCP

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - Data de emissão
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '117'
            dataEmissao = ET.SubElement(campoExtra1, 'valor')
            dataEmissao.text = naoContribuintesDia.loc[linha,
                                                       "Data de emissão"]

            # Valor total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorTotal
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            # conversaoData = pd.to_datetime(
            #     naoContribuintesDia.loc[linha, "Data de emissão"]).dt.date
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "RN":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'RN'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '22'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "RO":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'RO'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])

            # Valor Principal
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '83'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "RS":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'RS'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '22'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = naoContribuintesDia.loc[linha, "Valor UF Destino"]
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Convenio
            convenio = ET.SubElement(item, 'convenio')
            convenio.text = 'CONVENIO ICMS 93/2015'

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "SC":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'SC'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '24'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "Localizador"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "SE":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'SE'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '77'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento

            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        elif unidadeFederativa == "TO":

            # Dados da GNRE (TDados GNRE)
            dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
            dadosGNRE.attrib["versao"] = '2.00'

            ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
            ufFavorecida.text = 'TO'  # Inserir UF
            tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
            tipoGnre.text = '0'

            if naoContribuintesDia.loc[linha, 'Departamento'] == "BR0201":
                # Dados do Contribuinte SAO PAULO
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000253'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA ALVARENGA, 2025'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '50308'  # SP
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'SP'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '05509005'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '1130373900'

            else:
                # Dados do Contribuinte
                contribuinteEmitente = ET.SubElement(
                    dadosGNRE, 'contribuinteEmitente')
                identificacao = ET.SubElement(
                    contribuinteEmitente, 'identificacao')
                cnpj = ET.SubElement(identificacao, 'CNPJ')
                cnpj.text = '76881093000172'
                razaoSocial = ET.SubElement(
                    contribuinteEmitente, 'razaoSocial')
                razaoSocial.text = 'TROX DO BRASIL DIFUSAO DE AR ACUSTICA FILT. VENT. LTDA'
                endereco = ET.SubElement(contribuinteEmitente, 'endereco')
                endereco.text = 'RUA CYRO CORREIA PEREIRA, 300'
                municipio = ET.SubElement(contribuinteEmitente, 'municipio')
                municipio.text = '06902'  # Curitiba
                uf = ET.SubElement(contribuinteEmitente, 'uf')
                uf.text = 'PR'
                cep = ET.SubElement(contribuinteEmitente, 'cep')
                cep.text = '81170230'
                telefone = ET.SubElement(contribuinteEmitente, 'telefone')
                telefone.text = '4133168400'

            # Item GNRE
            itensGNRE = ET.SubElement(dadosGNRE, 'itensGNRE')
            item = ET.SubElement(itensGNRE, 'item')
            receita = ET.SubElement(item, 'receita')
            receita.text = '100102'

            # Tipo de documento
            documentoOrigem = ET.SubElement(item, 'documentoOrigem')
            documentoOrigem.attrib["tipo"] = '10'
            documentoOrigem.text = str(
                naoContribuintesDia.loc[linha, "NFE"])

            # Referencia
            referencia = ET.SubElement(item, 'referencia')
            referenciaMes = ET.SubElement(referencia, 'mes')
            referenciaMes.text = str(
                naoContribuintesDia.loc[linha, "Mês Referencia"])
            referenciaAno = ET.SubElement(referencia, 'ano')
            referenciaAno.text = str(
                naoContribuintesDia.loc[linha, "Ano Referencia"])

            # dataVencimento
            dataVencimento = ET.SubElement(item, 'dataVencimento')
            dataVencimento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

            # Valor Principal
            valorPagamento = str(
                naoContribuintesDia.loc[linha, "Valor UF Destino"])
            valorPrincipal = ET.SubElement(item, 'valor')
            valorPrincipal.attrib["tipo"] = '11'
            valorPrincipal.text = valorPagamento

            # Dados do Destinatario
            contribuinteDestinatario = ET.SubElement(
                item, 'contribuinteDestinatario')
            identificacaoDestinatario = ET.SubElement(
                contribuinteDestinatario, 'identificacao')

            if naoContribuintesDia.loc[linha, 'Tipo identificador fiscal'] == 'PJ':
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CNPJ')
            else:
                cnpjDestinatario = ET.SubElement(
                    identificacaoDestinatario, 'CPF')

            cnpjDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Entidade fiscal"])

            razaoSocialDestinatario = ET.SubElement(
                contribuinteDestinatario, 'razaoSocial')
            razaoSocialDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Razão Social"])

            municipioDestinatario = ET.SubElement(
                contribuinteDestinatario, 'municipio')
            municipioDestinatario.text = str(
                naoContribuintesDia.loc[linha, "Cidade"])

            # Campo Extra - CHNFE
            camposExtras = ET.SubElement(item, 'camposExtras')
            campoExtra1 = ET.SubElement(camposExtras, 'campoExtra')
            codigoCEX = ET.SubElement(campoExtra1, 'codigo')
            codigoCEX.text = '80'
            chaveNFE = ET.SubElement(campoExtra1, 'valor')
            chaveNFE.text = str(naoContribuintesDia.loc[linha, "Localizador"])

            # Valor Total
            valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
            valorGNRE.text = valorPagamento
            # Data Pagamento
            dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
            dataPagamento.text = str(
                naoContribuintesDia.loc[linha, "Data de vencimento"])

        linha = linha + 1


    now1 = datetime.now()
    formatted_date1 = now1.strftime('%d-%m-%Y %H:%M:%S')

    tree = ET.ElementTree(loteGNRE)
    tree.write("C:\\Users\\juan.santos\\Documents\\Juan\\Juan\\Gerador de GNRE\\static\\data\\xml\\loteGNRE.xml",
               xml_declaration=True, encoding='utf-8')

    #Gerando visual tabela
    nfe_table.to_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\Não Contribuintes Visual.xlsx", index=False)

    nfe_table1 = pd.read_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\Não Contribuintes Visual.xlsx")

    nfe_table1

   # Inserir mensagem abaixo da caixa
    return render_template("index.html", tables=[nfe_table1.to_html()], titles=[''])


@ app.route("/archive/xml", methods=["GET"])
def lista_arquivos():
    arquivos = []
    for nome_do_arquivo in os.listdir(DIRXML):
        endereco_arquivo = os.path.join(
            DIRXML, nome_do_arquivo)

        if (os.path.isfile(endereco_arquivo)):
            arquivos.append(nome_do_arquivo)

    return jsonify(arquivos)


@ app.route("/archive/xml/<nome_do_arquivo>", methods=["GET"])
def get_arquivo(nome_do_arquivo):

    return send_from_directory(DIRXML, nome_do_arquivo, as_attachment=True)


@ app.route("/archive/xlsx", methods=["GET"])
def lista_arquivos_xlsx():
    arquivos_xlsx = []
    for nome_do_arquivo_xlsx in os.listdir(DIRXLSX):
        endereco_arquivo_xlsx = os.path.join(
            DIRXLSX, nome_do_arquivo_xlsx)

        if (os.path.isfile(endereco_arquivo_xlsx)):
            arquivos_xlsx.append(nome_do_arquivo_xlsx)

    return jsonify(arquivos_xlsx)


@ app.route("/archive/xlsx/<nome_do_arquivo>", methods=["GET"])
def get_arquivo_xlsx(nome_do_arquivo_xlsx):

    return send_from_directory(DIRXLSX, nome_do_arquivo_xlsx, as_attachment=True)


@ app.route("/gerar-ap", methods=["POST"])
def gerar_ap():
    time.sleep(0.5)

    pa.PAUSE = 0.8

    naoContribuintesDia = pd.read_excel(
        r"C:\Users\juan.santos\Documents\Juan\Juan\Gerador de GNRE\static\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx", dtype=str)
    
    #formatando data como DD/MM/AAAA
    naoContribuintesDia["Data de emissão"] = pd.to_datetime(naoContribuintesDia["Data de emissão"])
    naoContribuintesDia["Data de emissão"] = naoContribuintesDia["Data de emissão"].dt.strftime('%d/%m/%Y')

    naoContribuintesDia["Data de vencimento"] = pd.to_datetime(naoContribuintesDia["Data de vencimento"])
    naoContribuintesDia["Data de vencimento"] = naoContribuintesDia["Data de vencimento"].dt.strftime('%d/%m/%Y')

    dataEmissao = naoContribuintesDia['Data de emissão']
    dataVencimento = naoContribuintesDia['Data de vencimento']
    
    naoContribuintesDia['Mês Referencia'] = naoContribuintesDia['Mês Referencia'].astype(
        'string')
    naoContribuintesDia['Ano Referencia'] = naoContribuintesDia['Ano Referencia'].astype(
        'string')

    codigoUF = naoContribuintesDia['UF']
    codigoFilial = naoContribuintesDia['Departamento']

    # naoContribuintesDia['Mês Referencia'] = naoContribuintesDia['Mês Referencia'].astype(
    #     'string')
    
    mesRef = naoContribuintesDia['Mês Referencia']

    print(naoContribuintesDia.dtypes)



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
    pa.moveTo(x=156, y=282)
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

            pa.write(str(aprovador))  # Aprovador
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

            pa.write(str(aprovador))  # Aprovador
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

            pa.write(str(aprovador))  # Aprovador
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
   
            pa.moveTo(x=32, y=194)  # Sair salvando
            pa.click()

    pa.moveTo(x=1893, y=137)
    pa.click()
    time.sleep(1)

    # Salvando GNREs

    for linha in naoContribuintesDia.index:

        if codigoUF[linha] == "AL":
            pa.moveTo(x=544, y=279)  # pesquisar gnre
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

            pa.moveTo(x=50, y=307)
            pa.click()

            pa.moveTo(x=1677, y=196)
            pa.click()

            pa.moveTo(x=1712, y=229)
            pa.click()

            pa.moveTo(x=472, y=704)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
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

            pa.moveTo(x=832, y=60) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("enter")
            pa.moveTo(x=378, y=188)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=30, y=195)
            pa.click()
            time.sleep(3)

            pa.moveTo(x=950, y=197)
            pa.click()
            time.sleep(10)
     

            # Fundo de combate a pobreza
            pa.moveTo(x=544, y=279)  # pesquisar gnre
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

            pa.moveTo(x=50, y=307)
            pa.click()

            pa.moveTo(x=1677, y=196)
            pa.click()

            pa.moveTo(x=1712, y=229)
            pa.click()

            pa.moveTo(x=472, y=704)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
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
            pa.moveTo(x=832, y=60) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"] + " FCP"))
            pa.press("enter")
            pa.moveTo(x=350, y=137)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=30, y=195)
            pa.click()
            time.sleep(3)


            pa.moveTo(x=950, y=197)
            pa.click()
            time.sleep(10)

        else:
            pa.moveTo(x=544, y=279)  # pesquisar gnre
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

            pa.moveTo(x=50, y=307)
            pa.click()

            pa.moveTo(x=1677, y=196)
            pa.click()

            pa.moveTo(x=1712, y=229)
            pa.click()

            pa.moveTo(x=472, y=704)
            pa.click()

            pa.moveTo(x=907, y=577)
            pa.click()
            time.sleep(2)

            pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
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
            pa.moveTo(x=832, y=60) #Pesquisar NF
            pa.click()
            pa.write(
                str(naoContribuintesDia.loc[linha, "NFE"]))
            pa.press("enter")
            pa.moveTo(x=410, y=137)
            pa.click()
            pa.press("enter")
            pa.moveTo(x=717, y=693)
            pa.click()
            pa.moveTo(x=30, y=195)
            pa.click()

            time.sleep(3)
            pa.moveTo(x=950, y=197)
            pa.click()
            time.sleep(8)

    pa.moveTo(x=1893, y=137)
    pa.click()
    time.sleep(1)

    # # Salvando GNRE no Protocolo

    # time.sleep(3)
    # pa.moveTo(x=30, y=167)
    # pa.click()
    # pa.press("tab")
    # time.sleep(0.3)
    # pa.hotkey('ctrl', 'a')
    # pa.write("cizlic507mt10")
    # pa.press("enter")
    # time.sleep(10)
    # pa.moveTo(x=727, y=989)
    # pa.click()
    # pa.moveTo(x=157, y=722)
    # pa.click()
    # pa.moveTo(x=30, y=167) #recolher pesquisa
    # pa.click()
    
    # pa.moveTo(x=736, y=194)#exibições
    # pa.click()

    # pa.moveTo(x=724, y=250) #Mostrar todas
    # pa.click()

    # pa.moveTo(x=1888, y=137)
    # pa.click()
    # time.sleep(1)


    # for linha in naoContribuintesDia.index:

    #     if codigoUF[linha] == "AL":
    #         pa.moveTo(x=869, y=347)  # pesquisar gnre
    #         time.sleep(1)
    #         pa.click()
    #         time.sleep(1)

    #         if codigoFilial[linha] == "BR0201":
    #             pa.write(str("BR02"))
    #         elif codigoFilial[linha] == "BR0101":
    #             pa.write(str("BR01"))
    #         elif codigoFilial[linha] == "BR0103":
    #             pa.write(str("BR01"))
    #         elif codigoFilial[linha] == "BR0104":
    #             pa.write(str("BR01"))
    #         elif codigoFilial[linha] == "BR0105":
    #             pa.write(str("BR01"))

    #         pa.press("tab")
    #         time.sleep(3)


    #         pa.moveTo(x=922, y=349)
    #         pa.click()

    #         pa.write(str(naoContribuintesDia.loc[linha, "NFE"]))  # Descrição

    #         pa.moveTo(x=844, y=377)
    #         pa.click()

    #         pa.moveTo(x=1712, y=229)
    #         pa.click()

    #         pa.moveTo(x=472, y=704)
    #         pa.click()

    #         pa.moveTo(x=907, y=577)
    #         pa.click()
    #         time.sleep(2)

    #         pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
    #         pa.click()

    #         if mesRef[linha] == "01":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "02":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")      
    #         elif mesRef[linha] == "03":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "04":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "05":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "06":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "07":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "08":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "09":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")        
    #         elif mesRef[linha] == "10":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "11":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "12":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")

    #         pa.press("enter")

    #         pa.moveTo(x=869, y=347) #Pesquisar NF
    #         pa.click()
    #         pa.write(
    #             str(naoContribuintesDia.loc[linha, "NFE"]))
    #         pa.press("enter")
    #         pa.moveTo(x=378, y=188)
    #         pa.click()
    #         pa.press("enter")
    #         pa.moveTo(x=717, y=693)
    #         pa.click()
    #         pa.moveTo(x=30, y=195)
    #         pa.click()
    #         time.sleep(3)

    #         pa.moveTo(x=950, y=197)
    #         pa.click()
    #         time.sleep(10)
     

    #         # Fundo de combate a pobreza
    #         pa.moveTo(x=914, y=694)
    #         pa.click()
    #         pa.moveTo(x=909, y=601)
    #         pa.click()
            
    #         pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
    #         pa.click()

    #         if mesRef[linha] == "01":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "02":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")      
    #         elif mesRef[linha] == "03":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "04":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "05":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "06":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "07":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "08":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "09":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")        
    #         elif mesRef[linha] == "10":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "11":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "12":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")

    #         pa.press("enter")
    #         pa.moveTo(x=832, y=60) #Pesquisar NF
    #         pa.click()
    #         pa.write(
    #             str(naoContribuintesDia.loc[linha, "NFE"] + " FCP"))
    #         pa.press("enter")
    #         pa.moveTo(x=350, y=137)
    #         pa.click()
    #         pa.press("enter")
    #         pa.moveTo(x=717, y=693)
    #         pa.click()
    #         pa.moveTo(x=30, y=195)
    #         pa.click()
    #         time.sleep(3)


    #         pa.moveTo(x=950, y=197)
    #         pa.click()
    #         time.sleep(10)

    #     else:
    #         pa.moveTo(x=869, y=347)  # pesquisar gnre
    #         time.sleep(1)
    #         pa.click()
    #         time.sleep(1)

    #         if codigoFilial[linha] == "BR0201":
    #             pa.write(str("DIFAL ICMS SP S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
    #                 naoContribuintesDia.loc[linha, "UF"]))  # Descrição
    #         elif codigoFilial[linha] == "BR0101":
    #             pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
    #                 naoContribuintesDia.loc[linha, "UF"]))  # Descrição
    #         elif codigoFilial[linha] == "BR0103":
    #             pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
    #                 naoContribuintesDia.loc[linha, "UF"]))  # Descrição
    #         elif codigoFilial[linha] == "BR0104":
    #             pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
    #                 naoContribuintesDia.loc[linha, "UF"]))  # Descrição
    #         elif codigoFilial[linha] == "BR0105":
    #             pa.write(str("DIFAL ICMS S/NF " + (naoContribuintesDia.loc[linha, "NFE"])) + " - " + (
    #                 naoContribuintesDia.loc[linha, "UF"]))  # Descrição
    #         pa.press("tab")

    #         pa.moveTo(x=50, y=307)
    #         pa.click()

    #         pa.moveTo(x=1677, y=196)
    #         pa.click()

    #         pa.moveTo(x=1712, y=229)
    #         pa.click()

    #         pa.moveTo(x=472, y=704)
    #         pa.click()

    #         pa.moveTo(x=907, y=577)
    #         pa.click()
    #         time.sleep(2)

    #         pa.moveTo(x=636, y=62) #Pesquisar caminho pasta
    #         pa.click()

    #         if mesRef[linha] == "01":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "02":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")      
    #         elif mesRef[linha] == "03":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "04":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "05":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "06":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "07":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "08":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "09":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")        
    #         elif mesRef[linha] == "10":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "11":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")
    #         elif mesRef[linha] == "12":
    #             textCopy = caminhoPasta + " " + naoContribuintesDia.loc[linha, "Ano Referencia"] + "\\" + naoContribuintesDia.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + naoContribuintesDia.loc[linha, "Ano Referencia"] 
    #             pyperclip.copy(textCopy)
    #             pa.hotkey("ctrl", "v")

    #         pa.press("enter")
    #         pa.moveTo(x=832, y=60) #Pesquisar NF
    #         pa.click()
    #         pa.write(
    #             str(naoContribuintesDia.loc[linha, "NFE"]))
    #         pa.press("enter")
    #         pa.moveTo(x=410, y=137)
    #         pa.click()
    #         pa.press("enter")
    #         pa.moveTo(x=717, y=693)
    #         pa.click()
    #         pa.moveTo(x=30, y=195)
    #         pa.click()

    #         time.sleep(3)
    #         pa.moveTo(x=950, y=197)
    #         pa.click()
    #         time.sleep(8)



    
    # pa.hotkey("ctrl", "w")
    # pa.press("enter")

    nfe_table1 = pd.read_excel(
        r"C:\Users\juan.santos\Desktop\Gerador de GNRE\static\data\Não Contribuintes Visual.xlsx")

    nfe_table1

    mensagem2 = "Processo concluído"

    return render_template("index.html", msg=mensagem2, tables=[nfe_table1.to_html()], titles=[''])


if __name__ == '__main__':
    # port = int(os.getenv('PORT'), '5000')
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
