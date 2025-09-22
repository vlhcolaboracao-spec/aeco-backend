
def parametroOutorgaOnerosa():
    zona = input("Informe a zona (ex: ZCT2, ZCT4): ").strip().upper()
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

    if zona in {"ZCT2", "ZCT4"} and avenida in avenidas_livres:
        return "livre"
    else:
        return "cobrança"

# Exemplo de uso
print(parametroOutorgaOnerosa())