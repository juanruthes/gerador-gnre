import xml.etree.ElementTree as ET
import pandas as pd

# arquivo dos nao contribuintes em CSV
naoContribuintesDia = pd.read_excel(
    r"C:\Users\juan.santos\Desktop\Gerador de GNRE\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx", dtype=str)

loteGNRE = ET.Element('TLote_GNRE')
loteGNRE.attrib["versao"] = '2.00'
loteGNRE.attrib["xmlns"] = 'http://www.gnre.pe.gov.br'
guias = ET.SubElement(loteGNRE, 'guias')

dataVcto = "2024-05-09"

linha = 0

for unidadeFederativa in naoContribuintesDia['Estado/Município']:

    if unidadeFederativa == "AL":
        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'AL'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

        # # GNRE 100129

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'AL'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

        # Valor Principal
        valorPrincipal = ET.SubElement(item, 'valor')
        valorPrincipal.attrib["tipo"] = '11'
        valorPrincipal.text = str(
            naoContribuintesDia.loc[linha, "Valor Fundo Combate Pobreza"])

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])
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
                                                 "Valor Fundo Combate Pobreza"]
        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "AC":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'AC'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        valorGNRE.text = naoContribuintesDia.loc[linha, "Valor Total DIFAL"]

        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "AM":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'AM'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])
        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = naoContribuintesDia.loc[linha, "Valor Total DIFAL"]

        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "AP":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'AP'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        contribuinteEmitente = ET.SubElement(dadosGNRE, 'contribuinteEmitente')
        identificacao = ET.SubElement(contribuinteEmitente, 'identificacao')
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

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        valorGNRE.text = naoContribuintesDia.loc[linha, "Valor Total DIFAL"]

        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "BA":
        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'BA'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
        valorGNRE.text = naoContribuintesDia.loc[linha, "Valor Total DIFAL"]
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "CE":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'CE'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

        # dataVencimento
        dataVencimento = ET.SubElement(item, 'dataVencimento')
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])

        # Valor GNRE
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = valorPagamento

        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "GO":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'GO'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "MA":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'MA'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "MG":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'MG'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

        dataVencimento = ET.SubElement(item, 'dataVencimento')
        dataVencimento.text = dataVcto

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "MS":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'MS'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "MT":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'MT'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])

        # Valor Total
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = valorPagamento

        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "PA":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'PA'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "PB":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'PB'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "PI":
        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'PI'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

        # dataVencimento
        dataVencimento = ET.SubElement(item, 'dataVencimento')
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])

        # Valor Total
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = valorPagamento

        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == 'RJ':

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        # UF Favorecida
        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'RJ'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

        valorPagamento = str(
            naoContribuintesDia.loc[linha, "Valor UF Destino"])

        # number_string_vlFcp = naoContribuintesDia.loc[linha, "Valor Fundo Combate Pobreza"]
        valorPagamentoFCP = str(naoContribuintesDia.loc[linha,
                                                        "Valor Fundo Combate Pobreza"])

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "RN":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'RN'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])

        # Valor Total
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = valorPagamento

        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "RO":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'RO'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "RS":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'RS'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

        municipioDestinatario = ET.SubElement(
            contribuinteDestinatario, 'municipio')
        municipioDestinatario.text = str(
            naoContribuintesDia.loc[linha, "Cidade"])

        # Valor Total
        valorGNRE = ET.SubElement(dadosGNRE, 'valorGNRE')
        valorGNRE.text = valorPagamento

        # Data Pagamento
        dataPagamento = ET.SubElement(dadosGNRE, 'dataPagamento')
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "SC":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'SC'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
        dataVencimento.text = dataVcto

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "SE":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'SE'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    elif unidadeFederativa == "TO":

        # Dados da GNRE (TDados GNRE)
        dadosGNRE = ET.SubElement(guias, 'TDadosGNRE')
        dadosGNRE.attrib["versao"] = '2.00'

        ufFavorecida = ET.SubElement(dadosGNRE, 'ufFavorecida')
        ufFavorecida.text = 'TO'  # Inserir UF
        tipoGnre = ET.SubElement(dadosGNRE, 'tipoGnre')
        tipoGnre.text = '0'

        if naoContribuintesDia.loc[linha, 'Departamento_x'] == "BR0201":
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
            naoContribuintesDia.loc[linha, "Número do documento_x"])

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
        dataVencimento.text = dataVcto

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
            naoContribuintesDia.loc[linha, "Unnamed: 11"])

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
        dataPagamento.text = dataVcto

    linha = linha + 1


tree = ET.ElementTree(loteGNRE)
tree.write('loteGNRE.xml', xml_declaration=True, encoding='utf-8')
