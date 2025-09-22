def parametroRecuoFrontal(zona, uso):
    # normaliza entradas
    zona = (zona or "").strip().upper()
    uso  = (uso  or "").strip().capitalize()  # "Residencial" / "Comercial"

    zonas_padrao = {"ZC1","ZC2","ZAD1","ZAD2","ZH2","ZH3","ZCT1","ZCT2","ZCT3"}

    if zona in zonas_padrao:
        if uso == "Residencial":
            valor = 4.0
        elif uso == "Comercial":
            valor = 1.5
        else:
            return f"⚠️ Uso {uso} não reconhecido."

    elif zona == "ZEIS":
        if uso == "Residencial":
            valor = 2.0
        elif uso == "Comercial":
            valor = 1.5
        else:
            return f"⚠️ Uso {uso} não reconhecido."

    else:
        return f"⚠️ Zona {zona} não encontrada."

    return valor



#zona = input("Digite a zona: ")
#uso = input("Digite o uso (Residencial ou Comercial): ")
#print(parametroRecuoFrontal(zona, uso, ID=None))
