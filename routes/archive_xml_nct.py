import os
from flask import Blueprint, jsonify

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
DIRXML = "static/data/xml"
DIRXLSX = "static/data/arquivo-nao-contribuinte"

archive_xml_nct_route = Blueprint('archive_xml_nct', __name__)

@ archive_xml_nct_route.route("/archive/xml", methods=["GET"])
def lista_arquivos():
    arquivos = []
    for nome_do_arquivo in os.listdir(DIRXML):
        endereco_arquivo = os.path.join(
            DIRXML, nome_do_arquivo)

        if (os.path.isfile(endereco_arquivo)):
            arquivos.append(nome_do_arquivo)

    return jsonify(arquivos)

