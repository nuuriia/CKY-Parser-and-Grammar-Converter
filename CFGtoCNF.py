def converttoCNF(grammar):
    """
    Converteix una gramàtica incontextual (CFG) a Chomsky Normal Form (CNF).
    
    Paràmetres:
        grammar : Una tupla que representa la gramàtica amb el diccionari de regles, el símbol inicial i el conjunt de terminals
    
    Retorna: La nova gramàtica en el mateix format

    """
    grammar_dict,start_symbol,terminals=grammar
    # 1 Nou símbol inicial
    change_start_symbol = False
    for _,valor in grammar_dict.items():
        for produccio in valor:
            if start_symbol in produccio:
                change_start_symbol = True
                break
        if change_start_symbol:
            break
    if change_start_symbol:
        grammar_dict['S0'] = [(start_symbol,)]
        start_symbol = 'S0'

    # 2 Elimina les produccions buides
    # Primer trobem tots aquells que generen la producció buida
    prod_buida = { regla for regla, produccions in grammar_dict.items() if () in produccions }
    # Afegim aquelles que generen la producció buida indirectament
    seguir = True
    while seguir:
        seguir = False
        for regla, produccions in grammar_dict.items():
            if any(all(x in prod_buida for x in produccio) for produccio in produccions):
                if regla not in prod_buida:
                    prod_buida.add(regla)
                    seguir = True

    # Eliminem les produccions buides 
    for regla, produccions in grammar_dict.copy().items():
        for produccio in produccions: # No .copy() aixi mira tots
            for i in range(len(produccio)):
                if produccio[i] in prod_buida:
                    new=produccio[:i] + produccio[i+1:]
                    if new not in produccions and new != (regla,):
                        produccions.append(produccio[:i] + produccio[i+1:])
        if () in produccions and regla!= start_symbol:
            produccions.remove(())

    
    # 3 Eliminem produccions unitàries
    unitaries = True
    while unitaries:
        unitaries = False
        for regla, produccions in grammar_dict.items():
            for produccio in produccions.copy():
                if len(produccio) == 1 and produccio[0] not in terminals:
                    nou = produccio[0]
                    produccions.remove(produccio) # eliminem la unitària A→B
                    for prod_B in grammar_dict[nou]: # afegim totes les produccions de B a A
                        if prod_B not in produccions and prod_B != (regla,):
                            produccions.append(prod_B)
                            if len(prod_B) == 1 and prod_B[0] not in terminals:
                                unitaries = True

    # 4 Eliminem produccions de més de dos símbols
    simbol_actual='0'
    produccions_afegides={}
    for _,valor in grammar_dict.copy().items():
        for i in range(len(valor)):    
            while len(valor[i])>2:
                produccio=valor[i]
                new=produccio[:2]
                if new in produccions_afegides:
                    valor[i]=(produccions_afegides[new],) + produccio[2:]
                else:
                    while f'X{simbol_actual}' in grammar_dict.keys():
                        simbol_actual+=1
                    grammar_dict[f'X{simbol_actual}']=[new]
                    produccions_afegides[new]=f'X{simbol_actual}'
                    valor[i] = (f'X{simbol_actual}',) + produccio[2:]
                    simbol_actual=str(int(simbol_actual)+1)

    # 5 Separem terminals de no terminals
    for _,valor in grammar_dict.copy().items():
        for i in range(len(valor)):
            produccio=valor[i]
            if len(produccio)>1:
                for j in range(len(produccio)):
                    e=produccio[j]
                    if e in terminals:
                        if e in produccions_afegides:
                            valor[i]= produccio[:j] + (produccions_afegides[e],) + produccio[j+1:]
                        else:
                            while f'X{simbol_actual}' in grammar_dict.keys():
                                simbol_actual+=1
                            grammar_dict[f'X{simbol_actual}']=[(e,)]
                            valor[i]=produccio[:j] + (f'X{simbol_actual}',) + produccio[j+1:]
                            produccions_afegides[e]=f'X{simbol_actual}'
                            simbol_actual=str(int(simbol_actual)+1) 
                                  
    return grammar_dict,start_symbol,terminals
                    
