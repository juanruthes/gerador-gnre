import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

upload_nct_route = Blueprint('upload_nct', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
DIRXML = "static/data/xml"
DIRXLSX = "static/data/arquivo-nao-contribuinte"

@ upload_nct_route.route("/data", methods=["POST"])
def data_upload_nct():
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
    return render_template("nao-contribuintes.html", msg=mensagem)
