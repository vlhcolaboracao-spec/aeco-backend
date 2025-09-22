def parametroTestada():
    zona = input("Informe a zona (ex: ZCT2, ZCT4, ZCS1...): ").strip().upper()
    natureza = input("Informe a natureza (desmembramento | loteamento e condominio): ").strip().lower()

    # dicionário de regras: (zona, natureza) -> valor do parâmetro
    regras = {
        ("ZAD1", "desmembramento"): 10.0,
        ("ZAD1", "loteamento e condominio"): 15.0,
        ("ZAD2", "desmembramento"): 10.0,
        ("ZAD2", "loteamento e condominio"): 15.0,
        ("ZH2", "desmembramento"): 10.0,
        ("ZH2", "loteamento e condominio"): 15.0,
        ("ZH3", "desmembramento"): 10.0,
        ("ZH3", "loteamento e condominio"): 12.0,
        ("ZCT2", "desmembramento"): 10.0,
        ("ZCT2", "loteamento e condominio"): 15.0,
        ("ZCT3", "desmembramento"): 10.0,
        ("ZCT3", "loteamento e condominio"): 15.0,
        ("ZCT4", "desmembramento"): 10.0,
        ("ZCT4", "loteamento e condominio"): 15.0,
        # adicione outras zonas aqui
    }

    parametro = regras.get((zona, natureza), "⚠️ combinação não encontrada")
    return parametro


# Exemplo de uso
print("Parâmetro:", parametroTestada())
