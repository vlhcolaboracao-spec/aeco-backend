def parametroAlturaMaximaPermitida(zona):
    # normaliza a zona (remove espaços e usa maiúsculas)
    zona = zona.strip().upper()

    # I Casos simples
    if zona == "ZC1":
        valor = 12
    elif zona == "ZC2":
        valor = 8
    elif zona == "ZII":
        valor = 2
        print ("Caso precise de mais pavimentos, consulte o CONDESS")
    elif zona in ["ZAD2", "ZCT1"]:
        valor = "livre"

    # II Zonas que dependem da avenida
    elif zona in ["ZCT2", "ZCT4"]:
        avenida = input(
            "Qual destas avenidas? Digite exatamente como abaixo, inclusive maiusculas e minusculas:\n"
            "Av. Porto Alegre | Av. dos Emigrantes | Av. Paulista | "
            "Av. Brasil | Av. Joao Natalino Brescansin | Av. Tancredo Neves\n> "
        ).strip()

        avenidas_livres = {
            "Av. Porto Alegre",
            "Av. dos Emigrantes",
            "Av. Paulista",
            "Av. Brasil",
            "Av. Joao Natalino Brescansin",
            "Av. Tancredo Neves",
        }

        if avenida in avenidas_livres:
            valor = "livre"
        else:
            valor = 12  # padrão quando não está na lista

    # III Zona não reconhecida
    else:
        valor = f"⚠️ Warning: Zona {zona} não encontrada. (ID: {ID})"

    return valor



# Exemplo de uso interativo:
# zona = input("Digite a zona: ")
# print(parametroAlturaMaximaPermitida(zona, ID))
