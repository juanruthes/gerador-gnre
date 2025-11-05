import pandas as pd

tabela = pd.read_excel(
    r"C:\Users\juan.santos\Desktop\Gerador de GNRE\static\data\arquivo-nao-contribuinte\Não Contribuintes.xlsx")

tabela.drop(["Referência fiscal",
             "Status transmissão",
             "Tipo doc. fiscal",
             "Localizador",
             "Departamento_x",
             "Entidade fiscal",
             "Cidade",
             "Tipo identificador fiscal",
             ],
            axis=1, inplace=True)


table_html = tabela.to_html()

print(table_html)
