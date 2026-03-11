
def CKY(paraula, gram):
    ''' 
    Algoritme CKY que indica si una paraula és generada per una gramàtica.

    Paràmetres:
        paraula: La paraula que es vol comprovar en format de string
        gram : Una tupla que representa la gramàtica amb el diccionari de regles, el símbol inicial i el conjunt de terminals
    
    Retorna: Un booleà que representa si la paraula és o no generada per la gramàtica
    
    '''
    gram,inicial,terminals=gram
    n=len(paraula)
    if n==0:
        res= () in gram[inicial]
        print(f'La gramàtica {'no'if not res else 'si'} genera la paraula.')
        return res  # Si la paraula és buida comprovem si la gramàtica té una producció buida per l'inicial
    # Generem un diccionari invertit: producció: {regles que la generen}
    inv_terminal={t: set() for t in terminals}
    inv_no_terminal={}
    for regla, produccions in gram.items():
        for produccio in produccions:
            if len(produccio)==1: # producció terminal: A -> a
                inv_terminal[produccio[0]].add(regla)
            else:  # producció no terminal: A -> (B, C)
                if produccio not in inv_no_terminal:  # si no està al diccionari crea un set buit
                    inv_no_terminal[produccio] = set()
                inv_no_terminal[produccio].add(regla) # L'hi afegeix la regla

    taula=[[set() for _ in range(n-i)] for i in range(n)] # Creem la taula de CKY amb conjunts buits
    # Omplim la primera fila amb les regles que generen els terminals
    for i  in range(n):
        if paraula[i] not in terminals: # Si la gramàtica no té el terminal, la paraula no pot ser generada
            print(f'La gramàtica no genera la paraula.')
            return False
        taula[i][0]=inv_terminal[paraula[i]]
    for y in range(1,n):
        for x in range(n-y):
            # Generem les produccions per a la cel·la (x,y)
            for pc in range(y):
                # Producte cartesià
                for prod1 in taula[x][pc]:
                    for prod2 in taula[x+pc+1][y-(pc+1)]:
                        if (prod1, prod2) in inv_no_terminal:
                            taula[x][y].update(inv_no_terminal[(prod1, prod2)])  # Afegim les regles que generen la producció (prod1, prod2)

    for row in taula:
        print([sorted(cell) for cell in row]) # Printem la taula resultant (no és necessari, però és útil pels jocs de prova)

    res= inicial in taula[0][n-1] # comprovem que el símbol terminal està a la última cel·la
    print(f'La gramàtica {'no'if not res else 'si'} genera la paraula.')
 
    return res
    