mesRef = planNCT['Mês Referencia']

if mesRef[linha] == "01":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JAN " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)     

if mesRef[linha] == "02":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE FEV " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)   
     
if mesRef[linha] == "03":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAR " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "04":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE ABR " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "05":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE MAI " + planNCT.loc[linha, "Ano Referencia"]
    print(caminhoPastaGNRE) 
if mesRef[linha] == "06":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUN " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "07":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE JUL " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "08":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE AGO " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "09":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE SET " + planNCT.loc[linha, "Ano Referencia"] 
if mesRef[linha] == "10":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE OUT " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "11":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE NOV " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)
if mesRef[linha] == "12":
    caminhoPastaGNRE = caminhoPasta + " " + planNCT.loc[linha, "Ano Referencia"] + "\\" + planNCT.loc[linha, "Mês Referencia"]  + ". ARQUIVO GNRE DEZ " + planNCT.loc[linha, "Ano Referencia"] 
    print(caminhoPastaGNRE)

print(caminhoPastaGNRE)