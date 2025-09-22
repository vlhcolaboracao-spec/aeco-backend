def parametroRecuoLateral():
    zona = input("Informe a zona (ex: ZCT2, ZCT4, ZCS1...): ").strip().upper()
    
    # Se for zona de transição (ZCT), pedir a zona atravessada
    if zona.startswith("ZCT"):
        zona_ref = input("Informe a zona ATRAVESSADA (com recuo estático, ex: ZIA1): ").strip().upper()
        # 1) TENTATIVA DE HERDAR RECÚO FIXO DO MONGO
        doc = col_zonas.find_one({"Zona": zona_ref, "status": "active"}, {"recuoLateral": 1})
        if doc and "recuoLateral" in doc:
            valor = _to_float(doc["recuoLateral"])
            if valor is not None:
                return f"{valor:.2f} m (recuo lateral FIXO herdado da zona {zona_ref})"
        # se não achou fixo, segue para a regra dinâmica usando a zona_ref
    else:
        zona_ref = zona
    
    try:
        pavimentos = int(input("Informe a quantidade de pavimentos: ").strip())
        altura = float(input("Informe a altura total do prédio em metros: ").strip())
    except ValueError:
        return "⚠️ Valor inválido para pavimentos ou altura"

    # Definição de grupos de zonas
    grupo_min_15 = {"ZC1", "ZC2", "ZAD1", "ZAD2", "ZH1", "ZH2", "ZH3", "ZHL", "ZEIS"}   # zonas onde mínimo é 1,5 m
    grupo_min_20 = {"ZI1", "ZI2"}   # zonas onde mínimo é 2,0 m

    if zona_ref in grupo_min_15:
        min_recuo = 1.5
    elif zona_ref in grupo_min_20:
        min_recuo = 2.0
    else:
        return f"⚠️ Zona {zona} não cadastrada em nenhuma regra."

    # Aplicação da regra
    if pavimentos <= 2:
        recuo = f"0 m (exceto se houver aberturas → mínimo {min_recuo:.2f} m)"
    else:
        recuo_calc = altura / 10
        recuo = max(recuo_calc, min_recuo)
        recuo = f"{recuo:.2f} m"

    return recuo


# Exemplo de uso
print("Recuo exigido:", parametroRecuoLateral())
