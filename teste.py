import pandas as pd
import pyautogui as pa
import time

time.sleep(1)
print(pa.position())


# naoContribuintesDia = pd.read_excel(
#     "static/data/arquivo-nao-contribuinte/Não Contribuintes.xlsx", dtype=str)

# # 1. Certifique-se de que a coluna é do tipo datetime
# naoContribuintesDia["Data de vencimento"] = pd.to_datetime(naoContribuintesDia["Data de vencimento"])

# # 2. Crie a coluna com a data somada
# naoContribuintesDia["Nova Data"] = naoContribuintesDia["Data de vencimento"] + pd.Timedelta(7, unit='D')