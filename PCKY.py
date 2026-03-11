def PCKY(paraula, gram):
    '''
    Algoritme CKY probabilístic que indica si una paraula és generada per una gramàtica i la seva probabilitat.

    Paràmetres:
        paraula: La paraula que es vol comprovar en format de string
        gram : Una tupla que representa la gramàtica amb el diccionari de regles, el símbol inicial i el conjunt de terminals
    
    Retorna: Un booleà que representa si la paraula és o no generada per la gramàtica i la probabilitat
    
    '''
    gram,inicial,terminals=gram
    n=len(paraula)
    # generem un diccionari invertit: producció: {(regla que la genera,probabilitat),(...)}
    paraula_buida=False
    prob_paraula_buida=0
    inv_terminal={t: set() for t in terminals}
    inv_no_terminal={}
    for regla, produccions in gram.items():
        for (produccio,prob) in produccions:
            if len(produccio)==1: # producció terminal: A -> (a,prob)
                inv_terminal[produccio[0]].add((regla,prob))
            else:
                clau=tuple(produccio)  # producció no terminal: A -> ((B, C),prob)
                if clau not in inv_no_terminal:  # si no està al diccionari crea un set buit
                    inv_no_terminal[clau] = set()
                    if produccio==() and regla==inicial:  # Si la producció és buida i és l'inicial, la paraula és buida
                        paraula_buida=True
                        prob_paraula_buida=prob 
                inv_no_terminal[clau].add((regla,prob)) # L'hi afegeix la regla 
    if len(paraula)==0:
        print(f"Pertany: {paraula_buida}, Probabilitat: {prob_paraula_buida:.5f}")
        return paraula_buida, prob_paraula_buida  # Si la paraula és buida, comprovem si la gramàtica té una producció buida per l'inicial

    taula=[[{} for _ in range(n-i)] for i in range(n)]
    for i  in range(n):
        if paraula[i] not in terminals: # Si la gramàtica no té el terminal, la paraula no pot ser generada
            print("Pertany: False, Probabilitat: 0")
            return False, 0
        for (regla,prob) in inv_terminal[paraula[i]]:
            taula[i][0][regla] = prob
    for y in range(1,n):
        for x in range(n-y):
            # Generem les produccions per a la cel·la (x,y)
            for pc in range(y):
                # Producte cartesià
                for prod1, prob1 in taula[x][pc].items():
                    for prod2, prob2 in taula[x+pc+1][y-(pc+1)].items():
                        if (prod1, prod2) in inv_no_terminal:
                            prob3= prob1 * prob2 
                            for (regla,prob) in inv_no_terminal[(prod1, prod2)]:
                                if regla not in taula[x][y]:
                                    taula[x][y][regla] = 0
                                
                                taula[x][y][regla]=max(taula[x][y][regla],prob3*prob)  # Afegim les regles que generen la producció (prod1, prod2) amb la probabilitat combinada


    for i in taula:
        for j in i:
            print(j, end=' ') # Printem la taula resultant (no és necessari, però és útil pels jocs de prova)
        print()
    final= inicial in taula[0][n-1] # comprovem que el símbol terminal està a la última cel·la
    prob=taula[0][n-1][inicial] if final else 0 # obtenim la probabilitat
    print(f"Pertany: {final}, Probabilitat: {prob:.5f}")
 
    return final,prob
